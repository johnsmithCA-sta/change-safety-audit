# Changelog — change-safety-audit

格式参考 Keep a Changelog；版本号语义化（主.次.修订）。

## [1.1.0] - 2026-08-29

可发现性与评测治理版本（依据 2026-08-29 体检报告，基线 73/100）。

### Added

- 新增 `## 触发词` 章节：19 条，覆盖删/改/备份/受管判定/上下文瘦身/互评六个意图簇。
- 新增 `evals/`：
  - `evals/trigger_eval.json` — 触发评估集（should_trigger 15 条 + should_not_trigger 8 条）。
  - `evals/case-01..08` — 8 个二元「该不该拦」用例（该拦 4 + 不该拦 4），pre-graded 模式，逐条附 SKILL.md 规则锚点证据。
- 新增「参考文档（何时读哪个）」表：3 个 references 各给出明确触发条件。
- 新增本 Changelog。

### Changed

- description 191 → 约 300 字符：补排他边界（「不适用于：新建文件、有测试覆盖的纯代码改动、临时文件与缓存清理、常规代码审查与性能评估」），触发词同步扩充。
- version 1.0.1 → 1.1.0。

### 备注

- `preflight --strict` 对 `password_format` 的 4 项命中为工具误报（技能名 `change-safety-audit` 的 kebab-case 被当作密码模式），发布时以 `--waive password_format` 豁免，不修改技能名。kit 侧修复另行跟踪。

## [1.0.1] - 2026-08-29

### Fixed

- description 自称构式修正（「按本文件的规则」→ 消除第一人称施动，desc-check 自称构式项通过）。

## [1.0.0] - 2026-08-29

### Added

- 初始化：三条铁律（受管判定 / md5 验收 / 固定名备份）、审计五步（量化/查重/扫凭据/定受管/写验收）、决策根（规则 vs 快照）、多 agent 互评判据；3 个 references + 1 个量化脚本。
- 双平台发布：GitHub v1.0.0（tag 签名 verified）+ SkillHub skillId 176705。
