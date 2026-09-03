# change-safety-audit · 变更安全审计

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg) ![Release](https://img.shields.io/badge/Release-v1.1.0-green.svg) ![SkillHub](https://img.shields.io/badge/SkillHub-@user_65c8c185%2Fchange-safety-audit-orange.svg)

**English** — Validation and anti-footgun rules to run *before* deleting or modifying files: managed-file detection, md5 falsifiable verification, entropy-safe backup naming, and context-injection slimming.

Two high-frequency, easy-to-regret operations: deleting things and changing things. This skill makes you **prove the change is safe before you make it**.

**Install / 安装**

```bash
skillhub install change-safety-audit --namespace user_65c8c185
# or / 或
git clone https://github.com/johnsmithCA-sta/change-safety-audit.git
```

---

删除或改动文件前的验证与防坑规则。

## 解决什么问题

两件高频且容易翻车的事：

1. **删/改文件**——你以为删掉了，结果它被平台重建；你以为改成功了，结果内容被重置回默认值
2. **上下文膨胀**——每会话固定注入的记忆文件越堆越大，却没人量化过它到底占多少

这个技能不帮你压缩上下文（那是别的工具做的事），它给你的是**判断框架和验证方法**——什么时候该删、删了怎么确认、改完怎么验收。

## 核心内容

### 三条铁律

1. **受管文件先判定** —— 有些文件删了会被平台重建，判定只能靠实验，且必须遵守观测窗口规则
2. **验收比对 md5** —— 文件"还在"不等于"内容没被改回默认值"
3. **备份用固定名同名覆盖** —— 备份名里带日期 = 必然熵增

### 观测窗口规则

> 对「某机制不存在」的判定，观测窗口必须 **≥ 该机制已知最大周期**。周期未知时，只能说「X 分钟内未观测到」，**不得下否定结论**。

这条来自一次真实返工：删除文件后观察 4.5 分钟未见重建就下结论"删即最终解"，第 11 分钟文件重生。

### 决策根：规则 vs 快照

| 类型 | 特征 | 处置 |
|---|---|---|
| 规则 | 该怎么做事 | 短，值得每会话注入 |
| 快照 | 项目进展到哪了 | 长，按需检索，不进固定注入 |

膨胀几乎全部来自把快照当规则塞进记忆。

## 用法

量化当前上下文开销：

```bash
python3 scripts/audit_tokens.py                       # 默认目标
python3 scripts/audit_tokens.py ~/.workbuddy/SOUL.md  # 指定文件
python3 scripts/audit_tokens.py --dir ~/.workbuddy    # 扫描目录
```

零第三方依赖，仅 Python 标准库。默认目标按 WorkBuddy 平台配置，其他平台改 `DEFAULT_TARGETS` 即可。

## 目录结构

```
SKILL.md                        主入口（44 行，聚焦单一用途）
scripts/audit_tokens.py         token 开销量化脚本
references/
  硬规则详解.md                  三条铁律的推导与踩坑实例
  审计模板.md                    检查清单、去重命令、产出模板
  互评判据.md                    多 agent 互评五判据与价值衰减曲线
```

采用渐进披露：SKILL.md 只放判断入口，详细推导按需加载。

## 何时不用

新建文件、有测试覆盖的代码改动、临时文件与缓存目录——这些场景没有重建风险或有现成验收手段，不需要本技能。

## 许可

MIT
