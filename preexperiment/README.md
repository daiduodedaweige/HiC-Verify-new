# RTL 错误版本预实验起始集

主交付为 **5 个模块及每模块 1 个独立错误 RTL 版本**，原始 `../rtl/` 不修改。
每个错误版本只在一个逻辑位置注入一种错误，保持模块名和端口不变。
另附 25 条参考检查，用于验证原版行为、检查场景可达性和错误版本的可检出性。

## 文件入口

- `selection.md`：模块、依赖、选择理由、修改位置和错误说明。
- `rtl_mutants/<mutant_id>/<模块名>.sv`：需要的错误 RTL。
- `rtl_mutants/<mutant_id>/mutation.diff`：与原版的差异。
- `rtl_mutants/<mutant_id>/metadata.json`：哈希、变异类型和对应检出目标。
- `rtl_mutants/<mutant_id>/files.f`：从仓库根目录使用的独立 RTL 文件集。
- `rtl_reference/`：冻结的原版，共 5 个 DUT 和 1 个 RAM 依赖。
- `assertions/reference/`：25 条参考检查器，仅为验证变异服务。
- `dataset.json`、`cases/`：完整目标、来源位置和版本信息。
- `environment.md`：基础环境及形式结果的适用范围。
- `results/summary.md`、`results/summary.json`：实际验证结果。
- `results/logs/`、`results/traces/`：工具日志和可达性/反例见证。

## 运行

在仓库根目录执行：

```bash
python3 preexperiment/scripts/generate.py
python3 preexperiment/scripts/check.py --jobs 2
```

需要 `yosys` 和 `slang` 在 PATH 中。检查前核对原始 RTL、冻结副本、依赖和变异版本的哈希。
查询超时和深度可用 `--help` 查看。单目标试跑例如：

```bash
python3 preexperiment/scripts/check.py --target Q1_01
```

单目标结果写入 `partial_summary.*`，不会覆盖完整检查摘要。

每个变异保留原模块名，必须使用对应 `files.f` 单独编译；不要将所有变异和原版一起加入同一个文件集。
使用其他支持 SVA 的工具时，可以分析该文件集，再分析对应 `assertions/reference/<target_id>.sv`，
并按 `environment.md` 设置时钟和复位。参考检查器含模块级 `bind`。
本地形式结果来自 Yosys，不是 JasperGold 的运行结果。

## 研究使用边界

这些是受控 RTL 变异，不是从真实历史缺陷收集的样本。
参考检查的局部契约来自 RTL 分析，来源标为 `rtl_derived_candidate_contract`，均待独立规格复核。
工具通过只证明记录的局部关系在声明环境下成立，不意味着整个原版模块正确。
变异反例证明相应差异可达且可被参考检查检出，不代表所有可能的断言都能检出该错误。
本批准备不调用外部 LLM，也不构成对现有修复方法错修率的测量。
