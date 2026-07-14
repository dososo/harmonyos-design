#!/usr/bin/env python3
"""校验规范 Markdown 文件集的内部相对链接有效性。

只扫描顶层规范 md 与 docs/、skills/、examples/、templates/；
不扫描嵌套副本或顶层旧散落文档。断链返回非零退出码。默认只读、不联网。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TOP_MD = ["README.md", "AGENTS.md", "CONTRIBUTING.md", "CHANGELOG.md", "SECURITY.md"]
SUBDIRS = ["docs", "skills", "examples", "templates"]


def check_links(root: Path) -> list[str]:
    """返回断裂链接列表（空表示全部有效）。"""
    targets: list[Path] = []
    for name in TOP_MD:
        p = root / name
        if p.is_file():
            targets.append(p)
    for sub in SUBDIRS:
        d = root / sub
        if d.is_dir():
            targets.extend(sorted(d.rglob("*.md")))

    errors: list[str] = []
    for md in targets:
        text = md.read_text(encoding="utf-8")
        for raw in LINK_RE.findall(text):
            target = raw.split("#", 1)[0].strip()
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (md.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{md.relative_to(root)} -> {raw}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 Markdown 内部相对链接")
    parser.add_argument("repo", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.repo.resolve()
    errors = check_links(root)
    if errors:
        print("发现断裂的内部链接：")
        for error in errors:
            print(f"- {error}")
        return 1
    print("所有内部相对链接有效。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
