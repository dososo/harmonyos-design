#!/usr/bin/env python3
"""校验 Agent Skill 的目录、frontmatter、长度和本地引用。"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass(frozen=True)
class SkillValidationResult:
    skill_count: int
    errors: list[str]


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("缺少 YAML frontmatter 起始分隔符 ---")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("缺少 YAML frontmatter 结束分隔符 ---") from exc
    raw = "\n".join(lines[1:end])
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("frontmatter 必须是映射对象")
    body = "\n".join(lines[end + 1 :])
    return data, body


def validate_skill_file(path: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = path.parent
    try:
        metadata, _ = parse_frontmatter(path)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        return [f"{path}: {exc}"]

    name = metadata.get("name")
    description = metadata.get("description")

    if not isinstance(name, str):
        errors.append(f"{path}: name 必须是字符串")
    else:
        if not (1 <= len(name) <= 64):
            errors.append(f"{path}: name 长度必须为 1–64")
        if not NAME_RE.fullmatch(name):
            errors.append(f"{path}: name 只能包含小写字母、数字和单连字符")
        if name != skill_dir.name:
            errors.append(f"{path}: name={name!r} 与目录名 {skill_dir.name!r} 不一致")

    if not isinstance(description, str):
        errors.append(f"{path}: description 必须是字符串")
    elif not (1 <= len(description) <= 1024):
        errors.append(f"{path}: description 长度必须为 1–1024 字符，当前 {len(description)}")

    allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    unknown = sorted(set(metadata) - allowed)
    if unknown:
        errors.append(f"{path}: frontmatter 包含未知字段：{', '.join(unknown)}")

    meta_map = metadata.get("metadata")
    if meta_map is not None:
        if not isinstance(meta_map, dict):
            errors.append(f"{path}: metadata 必须是映射")
        elif any(not isinstance(k, str) or not isinstance(v, str) for k, v in meta_map.items()):
            errors.append(f"{path}: metadata 的键和值必须都是字符串")

    line_count = len(path.read_text(encoding="utf-8").splitlines())
    if line_count > 500:
        errors.append(f"{path}: 共 {line_count} 行，超过 500 行建议上限")

    text = path.read_text(encoding="utf-8")
    for raw_target in LINK_RE.findall(text):
        target = raw_target.split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        target_path = (skill_dir / target).resolve()
        try:
            target_path.relative_to(skill_dir.resolve())
        except ValueError:
            errors.append(f"{path}: 引用越出 Skill 根目录：{raw_target}")
            continue
        if not target_path.exists():
            errors.append(f"{path}: 引用文件不存在：{raw_target}")
        if target.startswith("references/") and len(Path(target).parts) > 2:
            errors.append(f"{path}: references 引用层级过深：{raw_target}")

    return errors


def validate_skills(repo_root: Path) -> SkillValidationResult:
    skill_files = sorted((repo_root / "skills").glob("*/SKILL.md"))
    errors: list[str] = []
    if not skill_files:
        errors.append(f"{repo_root}: 未找到 skills/*/SKILL.md")
    for path in skill_files:
        errors.extend(validate_skill_file(path))
    return SkillValidationResult(skill_count=len(skill_files), errors=errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 HarmonyOS-Design Skills")
    parser.add_argument("repo", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = validate_skills(args.repo.resolve())
    if result.errors:
        print("Skill 校验失败：")
        for error in result.errors:
            print(f"- {error}")
        return 1
    print(f"Skill 校验通过：{result.skill_count} 个 Skill。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
