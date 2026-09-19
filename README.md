# change-safety-audit · 变更安全审计

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg) ![Release](https://img.shields.io/badge/Release-v1.3.1-green.svg) ![SkillHub](https://img.shields.io/badge/SkillHub-@user_65c8c185%2Fchange-safety-audit-orange.svg)

**English** — Validation and anti-footgun rules to run *before* deleting or modifying files: managed-file detection, md5 falsifiable verification, entropy-safe backup naming, context-injection slimming, and orchestration for splitting a batch of changes across multiple agents.

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

### 五条铁律

1. **受管文件先判定** —— 有些文件删了会被平台重建，判定只能靠实验，且必须遵守观测窗口规则
2. **验收比对 md5** —— 文件"还在"不等于"内容没被改回默认值"
3. **默认不留备份** —— 先问"这次操作可逆吗"：可逆就不留副本；要留则固定名同名覆盖，不写日期
4. **删除前查引用面** —— 全类型检索（不只 `*.md`），命中项逐条分「活引用 / 历史叙述 / 别名」；不做这一步，删掉的可能不是冗余、而是唯一副本
5. **改上游先枚举下游** —— 改会被二次加工的产物（推送文案 / 报表 / 导出文件）前先穷举消费者，验收走端到端 dry 跑

### 观测窗口规则

> 对「某机制不存在」的判定，观测窗口必须 **≥ 该机制已知最大周期**。周期未知时，只能说「X 分钟内未观测到」，**不得下否定结论**。

判据来自实践：窗口取小了，就会把「尚未发生」当成「不会发生」，据此得出的结论会被后来的事实推翻。

### 决策根：规则 vs 快照

| 类型 | 特征 | 处置 |
|---|---|---|
| 规则 | 该怎么做事 | 短，值得每会话注入 |
| 快照 | 项目进展到哪了 | 长，按需检索，不进固定注入 |

膨胀几乎全部来自把快照当规则塞进记忆。

### 批量改引用 / 归集搬家

1. **先圈定 root** —— 只圈活跃文档，显式排除注入层（追加型日志只追加不许覆写）、代码仓、历史归档目录
2. **归集四步** —— md5 清单当反向依据（不留备份副本）→ 分批移动 + 两侧校验 → 移完 grep 旧路径找指针 → 历史用一条注记覆盖

### 多 agent 并行改动的编排

要把一批改动分给多个 agent / 多个会话并行做：

1. **按「文件」切分，不按「条目」切分** —— 一个文件只能有一个写入者；条目常横跨多文件，须按文件边界重新归并。风险最高、要能反向验证的那部分留给自己做
2. **跨文件共享口径逐字下发** —— 同一个常量出现在两处以上就会漂，把口径原样粘进每份指令
3. **并行 Edit 竞态按常态处理** —— 同一文件上「读—改—写」必须串行，每条改动后回读确认
4. **要求对方报「没做到的」** —— 并点名硬约束（不重排既有编号、不写来源与日期、不动可写范围外的文件）

收尾的 **10 步终检序列只能由主 agent 做**，判据、清单与实测踩坑见 `references/并行编排与终检.md`。

## 用法

量化当前上下文开销：

```bash
python3 scripts/audit_tokens.py                       # 默认目标
python3 scripts/audit_tokens.py ~/.workbuddy/SOUL.md  # 指定文件
python3 scripts/audit_tokens.py --dir ~/.workbuddy    # 扫描目录
```

零第三方依赖，仅 Python 标准库。注入目录与身份文件按平台自动探测候选路径（只统计本机真实存在的那一组），也可以用 `--file` / `--dir` 显式指定。

## 目录结构

```
SKILL.md                        主入口（只放判断入口，细节按需加载）
scripts/audit_tokens.py         token 开销量化脚本（跨平台路径探测）
references/
  硬规则详解.md                  五条铁律的推导与踩坑实例
  审计模板.md                    检查清单、去重命令、产出模板、平台适配对照
  互评判据.md                    多 agent 互评五判据与价值衰减曲线
  并行编排与终检.md              并行改动的四条分工纪律、10 步终检序列
  文档归集.md                    批量改引用前圈定 root、归集四步、旧路径指针复查
```

采用渐进披露：SKILL.md 只放判断入口，详细推导按需加载。

## 何时不用

单个新建文件、有测试覆盖的代码改动、临时文件与缓存目录——这些场景没有重建风险或有现成验收手段，不需要本技能。

## 许可

MIT
