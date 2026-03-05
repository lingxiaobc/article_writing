"""
extract_outline.py — 从 Markdown 文章中提取大纲结构
用法：python scripts/extract_outline.py <文件路径>
"""

import sys
import re


def extract_outline(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print("=" * 40)
    print(f"文章大纲：{filepath}")
    print("=" * 40)

    found = False
    for line in lines:
        match = re.match(r'^(#{1,6})\s+(.+)', line.strip())
        if match:
            level = len(match.group(1))
            title = match.group(2)
            indent = "  " * (level - 1)
            prefix = ["─", "┬", "├", "│", "└", "◦"][min(level - 1, 5)]
            print(f"{indent}{prefix} {title}")
            found = True

    if not found:
        print("（未找到 Markdown 标题，文章可能不含标题层级）")

    print("=" * 40)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python extract_outline.py <文件路径>")
        sys.exit(1)
    extract_outline(sys.argv[1])
