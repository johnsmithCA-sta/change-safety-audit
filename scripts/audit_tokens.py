#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_tokens.py — 审计每会话固定注入的上下文 token 开销。

零第三方依赖，仅 Python 标准库。估算公式为粗估（中文 0.9 token/字，
英数符号 0.35 token/字符），用于比较与排序，不用于计费。

用法:
    python3 audit_tokens.py                        # 用内置默认目标
    python3 audit_tokens.py ~/.workbuddy/SOUL.md   # 指定一个或多个文件
    python3 audit_tokens.py --dir ~/.workbuddy     # 扫描目录下所有 .md
"""

import argparse
import os
import sys

# 按你的平台修改。常见位置：
#   WorkBuddy  ~/.workbuddy/{SOUL,IDENTITY,USER,MEMORY}.md
#   Claude     ~/.claude/CLAUDE.md
#   OpenClaw   各自工作空间的 memory 目录
DEFAULT_TARGETS = [
    ("SOUL.md", "~/.workbuddy/SOUL.md"),
    ("IDENTITY.md", "~/.workbuddy/IDENTITY.md"),
    ("USER.md", "~/.workbuddy/USER.md"),
    ("MEMORY.md", "~/.workbuddy/MEMORY.md"),
]

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
        targets = DEFAULT_TARGETS

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
