#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_tokens.py — 审计每会话固定注入的上下文 token 开销。

零第三方依赖，仅 Python 标准库。估算公式为粗估（中文 0.9 token/字，
英数符号 0.35 token/字符），用于比较与排序，不用于计费。

用法:
    python3 audit_tokens.py                        # 自动探测本机的身份 / 记忆文件
    python3 audit_tokens.py <路径> [<路径> ...]     # 指定一个或多个文件
    python3 audit_tokens.py --dir <注入目录>        # 扫描目录下所有 .md
"""

import argparse
import os
import sys

# 不绑定单一平台：候选按平台分组，运行时只取 **本机真实存在** 的那些。
# 其他平台 / 自建 Agent：把它的身份或记忆文件加进对应分组即可；
# 也可以完全不用默认值，直接用命令行传入路径。
PLATFORM_CANDIDATES = {
    "WorkBuddy": [
        "~/.workbuddy/SOUL.md",
        "~/.workbuddy/IDENTITY.md",
        "~/.workbuddy/USER.md",
        "~/.workbuddy/MEMORY.md",
    ],
    "Claude Code": [
        "~/.claude/CLAUDE.md",
    ],
}

CJK = 0.9    # 中文 token 系数
OTHER = 0.35  # 英数与符号 token 系数


def estimate(text):
    cjk = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
    return int(cjk * CJK + (len(text) - cjk) * OTHER)


def read(path):
    full = os.path.expanduser(path)
    if not os.path.exists(full):
        return ""
    try:
        with open(full, encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ""


def main():
    p = argparse.ArgumentParser(description="审计上下文注入的 token 开销")
    p.add_argument("paths", nargs="*", help="要审计的文件路径")
    p.add_argument("--dir", help="扫描该目录下所有 .md 文件")
    args = p.parse_args()

    targets = [(os.path.basename(os.path.expanduser(x)), x) for x in args.paths]

    if args.dir:
        d = os.path.expanduser(args.dir)
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                if name.endswith(".md"):
                    targets.append((name, os.path.join(d, name)))

    if not targets:
        candidates = [("%s/%s" % (plat, os.path.basename(p)), p)
                      for plat, paths in PLATFORM_CANDIDATES.items() for p in paths]
        targets = [(n, p) for n, p in candidates
                   if os.path.exists(os.path.expanduser(p))]
        if not targets:
            print("未在本机探测到已知平台的身份 / 记忆文件。")
            print("候选如下，请用命令行传入实际路径（或用 --dir 指定注入目录）：")
            for n, p in candidates:
                print("  %-28s %s" % (n, p))
            return 2

    total = 0
    missing = []
    print("%-28s%10s%10s" % ("文件", "字节", "tokens"))
    print("-" * 48)
    for name, path in targets:
        text = read(path)
        if not text:
            missing.append(path)
            continue
        t = estimate(text)
        total += t
        print("%-28s%10d%10d" % (name, len(text.encode("utf-8")), t))
    print("-" * 48)
    print("%-28s%10s%10d" % ("合计", "", total))

    if missing:
        print("\n未找到（路径不匹配或不适用本平台）:")
        for m in missing:
            print("  %s" % m)

    print("\n提示：自动生成的云端 profile 通常另占数千 tokens 且本地不可控，")
    print("      单独列出，勿混入本地优化成果。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
