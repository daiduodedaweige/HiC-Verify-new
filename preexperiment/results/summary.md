# 本地验证结果

范围：all_targets；目标：25；查询：60；符合预期：60。

原版参考检查要求归纳证明或组合 SAT 证明；覆盖检查要求找到实际触发见证。
每个错误 RTL 要求同一检查能给出具体反例，证明变异可触发且不等价。

另以共享输入的原版/变异版组合电路给出接口输出差异见证；无效队列数据不参与比较。

| 查询 | 预期 | 实际 | 检查 |
|---|---|---|---|
| Q1_01__reference__assert | proven | proven | 通过 |
| Q1_01__reference__cover | reachable | reachable | 通过 |
| Q1_01__reference__assert__M_Q1_PIPE | counterexample | counterexample | 通过 |
| Q1_02__reference__assert | proven | proven | 通过 |
| Q1_02__reference__cover | reachable | reachable | 通过 |
| Q1_03__reference__assert | proven | proven | 通过 |
| Q1_03__reference__cover | reachable | reachable | 通过 |
| Q1_04__reference__assert | proven | proven | 通过 |
| Q1_04__reference__cover | reachable | reachable | 通过 |
| Q1_05__reference__assert | proven | proven | 通过 |
| Q1_05__reference__cover | reachable | reachable | 通过 |
| Q6_01__reference__assert | proven | proven | 通过 |
| Q6_01__reference__cover | reachable | reachable | 通过 |
| Q6_02__reference__assert | proven | proven | 通过 |
| Q6_02__reference__cover | reachable | reachable | 通过 |
| Q6_03__reference__assert | proven | proven | 通过 |
| Q6_03__reference__cover | reachable | reachable | 通过 |
| Q6_04__reference__assert | proven | proven | 通过 |
| Q6_04__reference__cover | reachable | reachable | 通过 |
| Q6_05__reference__assert | proven | proven | 通过 |
| Q6_05__reference__cover | reachable | reachable | 通过 |
| Q6_05__reference__assert__M_Q6_WRAP | counterexample | counterexample | 通过 |
| ARB_01__reference__assert | proven | proven | 通过 |
| ARB_01__reference__cover | reachable | reachable | 通过 |
| ARB_02__reference__assert | proven | proven | 通过 |
| ARB_02__reference__cover | reachable | reachable | 通过 |
| ARB_03__reference__assert | proven | proven | 通过 |
| ARB_03__reference__cover | reachable | reachable | 通过 |
| ARB_04__reference__assert | proven | proven | 通过 |
| ARB_04__reference__cover | reachable | reachable | 通过 |
| ARB_04__reference__assert__M_ARB_ID | counterexample | counterexample | 通过 |
| ARB_05__reference__assert | proven | proven | 通过 |
| ARB_05__reference__cover | reachable | reachable | 通过 |
| EX_01__reference__assert | proven | proven | 通过 |
| EX_01__reference__cover | reachable | reachable | 通过 |
| EX_02__reference__assert | proven | proven | 通过 |
| EX_02__reference__cover | reachable | reachable | 通过 |
| EX_03__reference__assert | proven | proven | 通过 |
| EX_03__reference__cover | reachable | reachable | 通过 |
| EX_03__reference__assert__M_EX_TAG | counterexample | counterexample | 通过 |
| EX_04__reference__assert | proven | proven | 通过 |
| EX_04__reference__cover | reachable | reachable | 通过 |
| EX_05__reference__assert | proven | proven | 通过 |
| EX_05__reference__cover | reachable | reachable | 通过 |
| ENC_01__reference__assert | proven | proven | 通过 |
| ENC_01__reference__cover | reachable | reachable | 通过 |
| ENC_02__reference__assert | proven | proven | 通过 |
| ENC_02__reference__cover | reachable | reachable | 通过 |
| ENC_02__reference__assert__M_ENC_PRIORITY | counterexample | counterexample | 通过 |
| ENC_03__reference__assert | proven | proven | 通过 |
| ENC_03__reference__cover | reachable | reachable | 通过 |
| ENC_04__reference__assert | proven | proven | 通过 |
| ENC_04__reference__cover | reachable | reachable | 通过 |
| ENC_05__reference__assert | proven | proven | 通过 |
| ENC_05__reference__cover | reachable | reachable | 通过 |
| M_Q1_PIPE__interface_difference | counterexample | counterexample | 通过 |
| M_Q6_WRAP__interface_difference | counterexample | counterexample | 通过 |
| M_ARB_ID__interface_difference | counterexample | counterexample | 通过 |
| M_EX_TAG__interface_difference | counterexample | counterexample | 通过 |
| M_ENC_PRIORITY__interface_difference | counterexample | counterexample | 通过 |

所有结论限定于 environment.md 中的采样与复位模型。
局部契约仍待独立规格复核；本批数据不用于直接估计 LLM 错修率。
