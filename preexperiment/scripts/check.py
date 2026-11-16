#!/usr/bin/env python3
"""Check syntax and local formal evidence; never invokes an LLM service."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import re
import shutil
import subprocess
import time
from pathlib import Path

from generate import symbols


BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def instrument(source, target, variant, kind):
    """Lower only this dataset's comb, overlap and one-clock implications.

    This is NOT a general SVA translator. Each assertion is also syntax-checked
    in its concurrent form. The explicit cycle/reset model is in environment.md.
    """
    # Yosys' Verilog reader does not accept "priority if". This encoder's
    # chain has an explicit final else, so removing only this qualifier
    # preserves its complete two-state combinational truth table.
    if target["top"] == "PriorityEncoderOneHotLow8":
        source = source.replace("priority if(", "if(")
    p = target[variant]
    a, c = p["antecedent"], p["consequent"]
    if p["timing"] == "comb":
        check = f"!({a}) || ({c})"
        body = f"\n  (* keep *) wire pilot_active = ({a});\n  always @* assert ({check});\n"
    else:
        guard = "pilot_past_valid && !reset"
        if p["timing"] == "next":
            guard += " && !$past(reset)"
            a = f"$past({a})"
        check = f"!({a}) || ({c})"
        body = ("\n  reg pilot_past_valid = 1'b0;\n"
                "  always @(posedge clock) begin\n"
                "    pilot_past_valid <= 1'b1;\n"
                "    if (!pilot_past_valid) assume (reset);\n"
                "  end\n"
                "  (* keep *) reg pilot_active = 1'b0;\n"
                "  always @(posedge clock) begin\n"
                f"    pilot_active <= ({guard}) && ({a});\n"
                f"    if ({guard}) assert ({check});\n"
                "  end\n")
        for inv in target.get("proof_invariants", []):
            body += ("  always @(posedge clock)\n"
                     f"    if (pilot_past_valid && !reset) assert ({inv['expression']});\n")
    pos = source.rfind("endmodule")
    if pos < 0:
        raise ValueError("Missing endmodule")
    return source[:pos] + "\n// Observational pilot monitor; generated for this query.\n" + body + source[pos:]


def job(target, variant, kind, module, args, mutant=None):
    sid, top = target["target_id"], target["top"]
    tag = f"{sid}__{variant}__{kind}" + (f"__{mutant['mutant_id']}" if mutant else "")
    work = BASE / "results" / "work" / tag
    work.mkdir(parents=True, exist_ok=True)
    source_path = BASE / (mutant["path"] if mutant else module["reference"])
    generated = work / "design.sv"
    generated.write_text(instrument(source_path.read_text(), target, variant, kind))
    files = [str(generated)] + [str(BASE / "rtl_reference" / f) for f in module["dependencies"]]
    trace_dir = BASE / "results" / "traces"
    trace_dir.mkdir(parents=True, exist_ok=True)
    trace = trace_dir / f"{tag}.vcd"
    wavejson = trace_dir / f"{tag}.json"
    clocked = module["clocked"]
    prefix = (f"read_verilog -formal -sv {' '.join(files)}; "
              f"prep -top {top}; flatten; memory_map; async2sync; chformal -lower; dffunmap; opt_clean; ")
    if kind == "cover":
        # Coverage is queried separately; target assertions are not assumptions.
        prefix += "chformal -assert -remove; "
    common = f"-timeout {args.sat_timeout} -set-assumes -show-ports -show-regs -show pilot_active -dump_vcd {trace} -dump_json {wavejson}"
    if kind == "cover":
        command = f"sat {'-seq ' + str(args.depth) if clocked else ''} {common} -prove pilot_active 0 -falsify"
        expected = "reachable"
    elif mutant is not None:
        command = f"sat {'-seq ' + str(args.depth) if clocked else ''} {common} -prove-asserts -falsify"
        expected = "counterexample"
    else:
        induction = f"-seq 2 -tempinduct -maxsteps {args.induction}" if clocked else ""
        command = f"sat {induction} {common} -prove-asserts -verify"
        expected = "proven"
    script = work / "query.ys"
    script.write_text(prefix + command + "\n")
    log = BASE / "results" / "logs" / f"{tag}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    try:
        run = subprocess.run([args.yosys, "-Q", "-T", "-s", str(script)], capture_output=True, text=True, timeout=args.timeout)
        output, code = run.stdout + run.stderr, run.returncode
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        output = raw.decode(errors="replace") if isinstance(raw, bytes) else raw
        output += "\nPILOT_WALL_TIMEOUT\n"
        code = None
    log.write_text(output)
    # Require explicit solver evidence, not filenames or a zero exit status alone.
    has_cex = "SAT proof finished - model found: FAIL!" in output
    has_proof = ("Induction step proven: SUCCESS!" in output or
                 "SAT proof finished - no model found: SUCCESS!" in output)
    observed = ("reachable" if kind == "cover" else "counterexample") if has_cex else "proven" if has_proof else "unresolved"
    ok = code == 0 and observed == expected
    row = {"query_id": tag, "target_id": sid, "variant": variant, "kind": kind,
           "mutant_id": mutant["mutant_id"] if mutant else None,
           "expected": expected, "observed": observed, "passed": ok, "returncode": code,
           "seconds": round(time.monotonic() - started, 3),
           "bound": args.depth if expected != "proven" and clocked else None,
           "proof_method": ("temporal_induction" if clocked else "combinational_sat") if expected == "proven" else "bounded_witness" if clocked else "combinational_witness",
           "log": str(log.relative_to(BASE)), "query": str(script.relative_to(BASE)),
           "trace": str(trace.relative_to(BASE)) if trace.exists() else None,
           "source_sha256": sha(source_path), "monitor_sha256": sha(generated)}
    row["jointly_proved_invariants"] = target.get("proof_invariants", []) if kind == "assert" else []
    print(f"{'OK' if ok else 'ISSUE'} {tag}: {observed}", flush=True)
    return row


def interface_job(mutant, module, args):
    """Find an observable output difference using shared input stimuli."""
    top, mid = mutant["top"], mutant["mutant_id"]
    tag = mid + "__interface_difference"
    work = BASE / "results" / "work" / tag
    work.mkdir(parents=True, exist_ok=True)
    reference = (BASE / module["reference"]).read_text()
    modified = (BASE / mutant["path"]).read_text()
    header = reference[reference.index("module "):reference.index(");") + 2]
    widths = symbols(reference)
    ports = {"input": [], "output": []}
    for m in re.finditer(r"\b(input|output)\s+(.*?)(?=\b(?:input|output|inout)\b|\);)", header, re.S):
        chunk = re.sub(r"\[[^]]+\]|\b(?:wire|logic|reg)\b", "", m.group(2))
        ports[m.group(1)] += [n.strip() for n in chunk.split(",") if n.strip()]
    def declaration(n):
        return ((widths[n] + " ") if widths[n] else "") + n
    wrapper = "module pilot_miter(\n" + ",\n".join("  input wire " + declaration(n) for n in ports["input"]) + "\n);\n"
    for n in ports["output"]:
        for prefix in ["gold_", "bad_"]:
            wrapper += "  wire " + ((widths[n] + " ") if widths[n] else "") + prefix + n + ";\n"
    for instance, prefix in [("pilot_gold", "gold_"), ("pilot_bad", "bad_")]:
        bindings = [f".{n}({n})" for n in ports["input"]]
        bindings += [f".{n}({prefix}{n})" for n in ports["output"]]
        wrapper += f"  {instance} {prefix}dut ({', '.join(bindings)});\n"
    if top in {"Queue1_UInt8", "Queue6_UInt2"}:
        difference = ("(gold_io_enq_ready != bad_io_enq_ready) || "
                      "(gold_io_deq_valid != bad_io_deq_valid) || "
                      "(gold_io_deq_valid && bad_io_deq_valid && gold_io_deq_bits != bad_io_deq_bits)")
    elif top == "XsRRArbiter":
        difference = ("(gold_io_out_valid != bad_io_out_valid) || "
                      "(gold_io_in_0_ready != bad_io_in_0_ready) || (gold_io_in_1_ready != bad_io_in_1_ready) || "
                      "(gold_io_out_valid && bad_io_out_valid && gold_io_out_bits_TxnID != bad_io_out_bits_TxnID)")
    else:
        difference = " || ".join(f"(gold_{n} != bad_{n})" for n in ports["output"])
    wrapper += f"  (* keep *) wire pilot_difference = {difference};\n"
    if module["clocked"]:
        wrapper += ("  reg pilot_past_valid = 1'b0;\n"
                    "  always @(posedge clock) begin\n"
                    "    pilot_past_valid <= 1'b1;\n"
                    "    if (!pilot_past_valid) assume (reset);\n"
                    "    if (pilot_past_valid && !reset) assert (!pilot_difference);\n"
                    "  end\n")
    else:
        wrapper += "  always @* assert (!pilot_difference);\n"
    wrapper += "endmodule\n"
    reference = re.sub(r"\bmodule\s+" + top + r"\b", "module pilot_gold", reference, count=1)
    modified = re.sub(r"\bmodule\s+" + top + r"\b", "module pilot_bad", modified, count=1)
    if top == "PriorityEncoderOneHotLow8":
        reference = reference.replace("priority if(", "if(")
        modified = modified.replace("priority if(", "if(")
    design = work / "design.sv"
    design.write_text(reference + "\n" + modified + "\n" + wrapper)
    files = [str(design)] + [str(BASE / "rtl_reference" / f) for f in module["dependencies"]]
    trace = BASE / "results" / "traces" / (tag + ".vcd")
    wavejson = trace.with_suffix(".json")
    trace.parent.mkdir(parents=True, exist_ok=True)
    command = (f"read_verilog -formal -sv {' '.join(files)}; prep -top pilot_miter; "
               "flatten; memory_map; async2sync; chformal -lower; dffunmap; opt_clean; "
               f"sat {'-seq ' + str(args.depth) if module['clocked'] else ''} "
               f"-timeout {args.sat_timeout} -set-assumes -prove-asserts -falsify "
               f"-show-ports -show-public -show pilot_difference -dump_vcd {trace} -dump_json {wavejson}\n")
    script = work / "query.ys"
    script.write_text(command)
    started = time.monotonic()
    try:
        run = subprocess.run([args.yosys, "-Q", "-T", "-s", str(script)], capture_output=True, text=True, timeout=args.timeout)
        output, code = run.stdout + run.stderr, run.returncode
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        output = raw.decode(errors="replace") if isinstance(raw, bytes) else raw
        output += "\nPILOT_WALL_TIMEOUT\n"
        code = None
    log = BASE / "results" / "logs" / (tag + ".log")
    log.write_text(output)
    observed = "counterexample" if "SAT proof finished - model found: FAIL!" in output else "unresolved"
    row = {"query_id": tag, "target_id": mutant["target_id"], "variant": "original_vs_mutant",
           "kind": "interface_equivalence", "mutant_id": mid, "expected": "counterexample",
           "observed": observed, "passed": code == 0 and observed == "counterexample", "returncode": code,
           "seconds": round(time.monotonic() - started, 3), "bound": args.depth if module["clocked"] else None,
           "proof_method": "shared_input_output_difference", "observable_difference": difference,
           "log": str(log.relative_to(BASE)), "query": str(script.relative_to(BASE)),
           "trace": str(trace.relative_to(BASE)) if trace.exists() else None}
    print(f"{'OK' if row['passed'] else 'ISSUE'} {tag}: {observed}", flush=True)
    return row


def syntax_check(data, args):
    results = []
    for top, m in data["modules"].items():
        files = [BASE / m["reference"]] + [BASE / "rtl_reference" / f for f in m["dependencies"]]
        targets = [p for p in data["targets"] if p["top"] == top]
        for p in targets:
            files.append(BASE / "assertions" / "reference" / (p["target_id"] + ".sv"))
        result = subprocess.run([args.slang, "--lint-only", "--top", top, *map(str, files)], capture_output=True, text=True, timeout=args.timeout)
        log = BASE / "results" / "logs" / f"syntax_{top}.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(result.stdout + result.stderr)
        row = {"top": top, "passed": result.returncode == 0, "log": str(log.relative_to(BASE))}
        results.append(row)
        print(f"{'OK' if row['passed'] else 'ISSUE'} SVA syntax: {top}", flush=True)
    for mutant in data["rtl_mutants"]:
        top = mutant["top"]
        files = [BASE / mutant["path"]] + [BASE / "rtl_reference" / d for d in data["modules"][top]["dependencies"]]
        result = subprocess.run([args.slang, "--lint-only", "--top", top, *map(str, files)], capture_output=True, text=True, timeout=args.timeout)
        log = BASE / "results" / "logs" / f"syntax_{mutant['mutant_id']}.log"
        log.write_text(result.stdout + result.stderr)
        row = {"mutant_id": mutant["mutant_id"], "passed": result.returncode == 0, "log": str(log.relative_to(BASE))}
        results.append(row)
        print(f"{'OK' if row['passed'] else 'ISSUE'} RTL syntax: {mutant['mutant_id']}", flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--depth", type=int, default=16)
    parser.add_argument("--induction", type=int, default=20)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--sat-timeout", type=int, default=15)
    parser.add_argument("--target", action="append", help="Only run selected target(s); summary is explicitly partial")
    parser.add_argument("--yosys", default=shutil.which("yosys"))
    parser.add_argument("--slang", default=shutil.which("slang"))
    args = parser.parse_args()
    if not args.yosys or not args.slang:
        parser.error("yosys and slang must be available")
    data = json.loads((BASE / "dataset.json").read_text())
    for top, m in data["modules"].items():
        if sha(BASE / m["reference"]) != m["source_sha256"]:
            raise SystemExit(f"Frozen source changed: {top}")
        if sha(ROOT / m["original"]) != m["source_sha256"]:
            raise SystemExit(f"Original RTL changed; review and regenerate dataset: {top}")
        for dep, expected_hash in m["dependency_sha256"].items():
            if sha(BASE / "rtl_reference" / dep) != expected_hash or sha(ROOT / "rtl" / dep) != expected_hash:
                raise SystemExit(f"Dependency changed: {dep}")
    for m in data["rtl_mutants"]:
        if sha(BASE / m["path"]) != m["mutant_sha256"]:
            raise SystemExit(f"Mutation changed: {m['mutant_id']}")
    syntax = syntax_check(data, args)
    if not all(r["passed"] for r in syntax):
        raise SystemExit("SVA syntax failed; inspect results/logs/syntax_*.log")
    selected = [p for p in data["targets"] if not args.target or p["target_id"] in args.target]
    if args.target and set(args.target) != {p["target_id"] for p in selected}:
        parser.error("Unknown --target")
    jobs = []
    for p in selected:
        m = data["modules"][p["top"]]
        jobs.extend([(p, "reference", "assert", m, None), (p, "reference", "cover", m, None)])
        for mutant in data["rtl_mutants"]:
            if mutant["target_id"] == p["target_id"]:
                jobs.append((p, "reference", "assert", m, mutant))
    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(job, p, v, k, m, args, mu) for p, v, k, m, mu in jobs]
        for mutant in data["rtl_mutants"]:
            if any(p["target_id"] == mutant["target_id"] for p in selected):
                futures.append(pool.submit(interface_job, mutant, data["modules"][mutant["top"]], args))
        rows = [f.result() for f in futures]
    summary = {"scope": "selected_targets" if args.target else "all_targets", "targets_checked": len(selected),
               "jobs": len(rows), "passed": sum(r["passed"] for r in rows),
               "seconds": round(time.monotonic() - started, 3), "syntax": syntax,
               "tools": {"yosys": subprocess.check_output([args.yosys, "-V"], text=True).strip(),
                         "slang": subprocess.check_output([args.slang, "--version"], text=True).strip()},
               "configuration": {k: v for k, v in vars(args).items()}, "results": rows,
               "interpretation": "Cycle-model reference checks and reachable RTL mutation counterexamples; no external-spec certification."}
    result_path = BASE / "results" / ("partial_summary.json" if args.target else "summary.json")
    result_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    report = ["# 本地验证结果", "", f"范围：{summary['scope']}；目标：{len(selected)}；查询：{len(rows)}；符合预期：{summary['passed']}。", "",
              "原版参考检查要求归纳证明或组合 SAT 证明；覆盖检查要求找到实际触发见证。",
              "每个错误 RTL 要求同一检查能给出具体反例，证明变异可触发且不等价。", "",
              "另以共享输入的原版/变异版组合电路给出接口输出差异见证；无效队列数据不参与比较。", "",
              "| 查询 | 预期 | 实际 | 检查 |", "|---|---|---|---|"]
    for r in rows:
        report.append(f"| {r['query_id']} | {r['expected']} | {r['observed']} | {'通过' if r['passed'] else '待处理'} |")
    report += ["", "所有结论限定于 environment.md 中的采样与复位模型。",
               "局部契约仍待独立规格复核；本批数据不用于直接估计 LLM 错修率。", ""]
    report_path = result_path.with_suffix(".md")
    report_path.write_text("\n".join(report))
    print(f"Completed: {summary['passed']}/{len(rows)} checks; {result_path}")
    if summary["passed"] != len(rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
