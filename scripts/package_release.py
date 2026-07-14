#!/usr/bin/env python3
"""重新生成发布清单 MANIFEST.json 与 SHA256SUMS.txt。

只纳入规范交付文件；排除清单自身、评测产物、嵌套副本、构建产物与顶层冗余物。
默认只读地计算并覆盖写出两份清单，不修改其他文件、不联网。
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from validate_evals import validate_evals
from validate_rules import validate_rules
from validate_skills import validate_skills

# 顶层文件白名单（存在才纳入）
TOP_FILES = [
    ".gitignore", "CHANGELOG.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md",
    "LICENSE", "NOTICE", "README.md", "README.en.md", "SECURITY.md",
    "VERSION", "pyproject.toml",
]
# 递归纳入的目录及其后缀过滤
DIR_GLOBS = {
    ".github": ("*.yml", "*.yaml"),
    "docs": ("*.md",),
    "rules": ("*.yaml", "*.json"),
    "evals": ("*.json", "*.ets"),   # 含 fixtures/*.ets；evals/results 另行排除
    "skills": ("*.md",),
    "scripts": ("*.py",),
    "tests": ("*.py",),
    "templates": ("*.md",),
    "examples": ("*.ets", "*.md"),
}
# 明确排除的路径片段（相对仓库根）
EXCLUDE_PARTS = {"results", "__pycache__"}


def collect_files(root: Path) -> list[Path]:
    """按白名单收集规范交付文件，返回相对根排序后的路径列表。"""
    files: list[Path] = []
    for name in TOP_FILES:
        p = root / name
        if p.is_file():
            files.append(p)
    for subdir, patterns in DIR_GLOBS.items():
        base = root / subdir
        if not base.is_dir():
            continue
        for pattern in patterns:
            for p in base.rglob(pattern):
                rel_parts = set(p.relative_to(root).parts)
                if rel_parts & EXCLUDE_PARTS:
                    continue
                if p.is_file():
                    files.append(p)
    # 去重并按相对路径字符串排序，保证清单稳定
    uniq = sorted(set(files), key=lambda x: str(x.relative_to(root)))
    return uniq


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(root: Path, version: str, tests: str) -> dict:
    skill_r = validate_skills(root)
    rule_r = validate_rules(root)
    eval_r = validate_evals(root)
    files = collect_files(root)
    entries = [
        {
            "path": str(p.relative_to(root)),
            "size": p.stat().st_size,
            "sha256": sha256_of(p),
        }
        for p in files
    ]
    return {
        "name": "HarmonyOS-Design",
        "version": version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "skills": skill_r.skill_count,
            "rules": rule_r.rule_count,
            "sources": rule_r.source_count,
            "trigger_evals": eval_r.trigger_count,
            "positive_trigger_evals": eval_r.positive_count,
            "negative_trigger_evals": eval_r.negative_count,
            "review_evals": eval_r.review_count,
            "tests": tests,
        },
        "files": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="重新生成 MANIFEST.json 与 SHA256SUMS.txt")
    parser.add_argument("repo", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--version", default="0.2.0-draft", help="发布版本标签")
    parser.add_argument("--tests", default="未运行", help="测试结果摘要，如 '7 passed'")
    parser.add_argument("--check", action="store_true", help="仅比对现有清单是否与实际一致，不写出")
    args = parser.parse_args()
    root = args.repo.resolve()

    manifest = build_manifest(root, args.version, args.tests)

    if args.check:
        current = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
        cur_files = {f["path"]: f["sha256"] for f in current.get("files", [])}
        new_files = {f["path"]: f["sha256"] for f in manifest["files"]}
        added = sorted(set(new_files) - set(cur_files))
        removed = sorted(set(cur_files) - set(new_files))
        changed = sorted(p for p in cur_files.keys() & new_files.keys() if cur_files[p] != new_files[p])
        if added or removed or changed:
            print("清单与实际不一致：")
            for p in added:
                print(f"  + 新增 {p}")
            for p in removed:
                print(f"  - 缺失 {p}")
            for p in changed:
                print(f"  * 变更 {p}")
            return 1
        print(f"清单一致：{len(new_files)} 个文件。")
        return 0

    (root / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [f"{f['sha256']}  {f['path']}" for f in manifest["files"]]
    (root / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"已生成 MANIFEST.json 与 SHA256SUMS.txt：{len(manifest['files'])} 个文件，版本 {args.version}。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
