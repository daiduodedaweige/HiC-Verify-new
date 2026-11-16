#!/usr/bin/env python3
"""Generate isolated RTL mutants and their reference-checking material."""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "preexperiment"


def write(path, content):
    path = OUT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def symbols(source):
    """Read the simple scalar/vector declarations in the selected RTL."""
    header = source[source.index("module "):source.index(");") + 2]
    result = {}
    for m in re.finditer(r"\b(?:input|output|inout)\s+(.*?)(?=\b(?:input|output|inout)\b|\);)", header, re.S):
        chunk = re.sub(r"\b(?:logic|wire|reg|signed|unsigned)\b", "", m.group(1)).strip()
        width = re.match(r"\[[^]]+\]", chunk)
        packed = width.group(0) if width else ""
        if width:
            chunk = chunk[width.end():]
        for name in chunk.split(","):
            name = name.strip()
            if re.fullmatch(r"[A-Za-z_]\w*", name):
                result[name] = packed
    for m in re.finditer(r"\b(?:wire|reg|logic)\s*(\[[^]]+\])?\s*(\w+)\s*[,;=]", source):
        result[m.group(2)] = m.group(1) or ""
    return result


def checker(p, source):
    v = p["reference"]
    top, sid = p["top"], p["target_id"]
    table = symbols(source)
    expression = v["antecedent"] + " " + v["consequent"]
    expression += " " + " ".join(i["expression"] for i in p.get("proof_invariants", []))
    names = sorted(n for n in table if re.search(r"\b" + re.escape(n) + r"\b", expression))
    if v["timing"] != "comb":
        names = ["clock", "reset"] + [n for n in names if n not in {"clock", "reset"}]
    declarations = ",\n".join("  input wire " + ((table[n] + " ") if table[n] else "") + n for n in names)
    name = f"pilot_{sid}_reference"
    a, c = v["antecedent"], v["consequent"]
    if v["timing"] == "comb":
        body = f"  always_comb begin\n    a_target: assert (!({a}) || ({c}));\n    c_trigger: cover ({a});\n  end\n"
    else:
        op = "|=>" if v["timing"] == "next" else "|->"
        body = (f"  a_target: assert property (@(posedge clock) disable iff (reset)\n"
                f"    ({a}) {op} ({c}));\n"
                f"  c_trigger: cover property (@(posedge clock) disable iff (reset) ({a}));\n")
        for inv in p.get("proof_invariants", []):
            body += (f"  a_{inv['name']}: assert property (@(posedge clock) disable iff (reset)\n"
                     f"    ({inv['expression']}));\n")
    binding = ", ".join(f".{n}({n})" for n in names)
    return (f"// {sid}: {p['title']}\n// source_type: rtl_derived_candidate_contract\n"
            "// External specification review is pending.\n"
            f"module {name}(\n{declarations}\n);\n{body}endmodule\n"
            f"bind {top} {name} checker_{sid}_reference ({binding});\n")


def main():
    catalog = json.loads((OUT / "catalog.json").read_text())
    modules = {}
    for top, info in catalog["modules"].items():
        original = ROOT / "rtl" / f"{top}.sv"
        source = original.read_text()
        write(f"rtl_reference/{top}.sv", source)
        for dep in info["dependencies"]:
            write(f"rtl_reference/{dep}", (ROOT / "rtl" / dep).read_text())
        modules[top] = dict(info, original=str(original.relative_to(ROOT)),
                            source_sha256=digest(source), lines=len(source.splitlines()),
                            reference=f"rtl_reference/{top}.sv",
                            dependency_sha256={d: digest((ROOT / "rtl" / d).read_text()) for d in info["dependencies"]})

    for p in catalog["targets"]:
        sid, top = p["target_id"], p["top"]
        source = (ROOT / "rtl" / f"{top}.sv").read_text()
        write(f"assertions/reference/{sid}.sv", checker(p, source))
        write_json(f"cases/{sid}/target.json", p)

    mutants = []
    for definition in catalog["mutations"]:
        mid, top = definition["mutant_id"], definition["top"]
        old, new = definition["before"], definition["after"]
        source = (ROOT / "rtl" / f"{top}.sv").read_text()
        if source.count(old) != 1:
            raise ValueError(f"{mid}: mutation anchor must occur exactly once")
        modified = source.replace(old, new, 1)
        write(f"rtl_mutants/{mid}/{top}.sv", modified)
        patch = "".join(difflib.unified_diff(source.splitlines(True), modified.splitlines(True),
                                           fromfile=f"rtl_reference/{top}.sv", tofile=f"rtl_mutants/{mid}/{top}.sv"))
        write(f"rtl_mutants/{mid}/mutation.diff", patch)
        m = {"mutant_id": mid, "target_id": definition["target_id"], "top": top,
             "description": definition["description"], "path": f"rtl_mutants/{mid}/{top}.sv",
             "source_sha256": digest(source), "mutant_sha256": digest(modified),
             "changed_line": source[:source.index(old)].count("\n") + 1,
             "role": "controlled_rtl_mutation", "validation_status": "see results/summary.json"}
        write_json(f"rtl_mutants/{mid}/metadata.json", m)
        files = [f"preexperiment/rtl_mutants/{mid}/{top}.sv"]
        files += [f"preexperiment/rtl_reference/{d}" for d in modules[top]["dependencies"]]
        write(f"rtl_mutants/{mid}/files.f", "\n".join(files) + "\n")
        mutants.append(m)

    write_json("dataset.json", {"schema_version": 1, "modules": modules, "targets": catalog["targets"],
                               "rtl_mutants": mutants,
                               "provenance": "Controlled RTL mutants; local reference contracts await external-spec review."})
    rows = ["# 预实验模块选择", "", "按无依赖或单依赖、单时钟、小状态空间和可定位局部修改选取。", "",
            "| 模块 | 行数 | 类别 | 依赖 | 选择理由 |", "|---|---:|---|---|---|"]
    for top, m in modules.items():
        rows.append(f"| {top} | {m['lines']} | {m['category']} | {', '.join(m['dependencies']) or '无'} | {m['reason']} |")
    rows += ["", "## 行为边界", ""]
    for top, m in modules.items():
        rows.append(f"- **{top}**：{m['notes']}")
    rows += ["", "## 独立错误版本", "", "| 变异编号 | 模块 | 修改位置 | 注入错误 | 检出目标 |",
             "|---|---|---:|---|---|"]
    for m in mutants:
        rows.append(f"| {m['mutant_id']} | {m['top']} | {m['changed_line']} | {m['description']} | {m['target_id']} |")
    rows += ["", "每模块 1 个独立 RTL 错误版本；每模块另附 5 条参考检查，共 25 条。",
             "这些检查用于验证局部行为差异；契约来自 RTL 分析，尚需独立规格复核。", ""]
    write("selection.md", "\n".join(rows))
    print(f"Generated {len(modules)} reference modules, {len(mutants)} RTL mutants and {len(catalog['targets'])} reference checks.")


if __name__ == "__main__":
    main()
