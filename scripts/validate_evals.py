#!/usr/bin/env python3
"""校验触发 Eval、Review Eval 和 fixture 引用。"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class EvalValidationResult:
    trigger_count: int
    positive_count: int
    negative_count: int
    review_count: int
    errors: list[str]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evals(repo_root: Path) -> EvalValidationResult:
    trigger_path = repo_root / "evals" / "trigger-evals.json"
    review_path = repo_root / "evals" / "review-evals.json"
    rules_path = repo_root / "rules" / "harmony-design-rules.yaml"
    errors: list[str] = []

    for path in (trigger_path, review_path, rules_path):
        if not path.exists():
            errors.append(f"缺少文件：{path}")
    if errors:
        return EvalValidationResult(0, 0, 0, 0, errors)

    try:
        trigger_data = load_json(trigger_path)
        review_data = load_json(review_path)
        rules_data = yaml.safe_load(rules_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError) as exc:
        return EvalValidationResult(0, 0, 0, 0, [f"读取 Eval 失败：{exc}"])

    trigger_cases = trigger_data.get("cases", []) if isinstance(trigger_data, dict) else []
    review_cases = review_data.get("cases", []) if isinstance(review_data, dict) else []
    rule_ids = {item.get("id") for item in rules_data.get("rules", []) if isinstance(item, dict)}

    seen_trigger: set[str] = set()
    positive = negative = 0
    for case in trigger_cases:
        if not isinstance(case, dict):
            errors.append("trigger-evals 存在非对象 case")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append("trigger case 缺少 id")
            continue
        if case_id in seen_trigger:
            errors.append(f"trigger case ID 重复：{case_id}")
        seen_trigger.add(case_id)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{case_id}: prompt 不能为空")
        if not isinstance(case.get("should_trigger"), bool):
            errors.append(f"{case_id}: should_trigger 必须为布尔值")
        elif case["should_trigger"]:
            positive += 1
        else:
            negative += 1
        if not isinstance(case.get("reason"), str) or not case["reason"].strip():
            errors.append(f"{case_id}: reason 不能为空")
        if not isinstance(case.get("tags"), list) or not case["tags"]:
            errors.append(f"{case_id}: tags 必须为非空数组")

    if positive < 20:
        errors.append(f"正触发案例不足：{positive}，至少 20")
    if negative < 20:
        errors.append(f"负触发案例不足：{negative}，至少 20")

    seen_review: set[str] = set()
    severities = {"blocker", "major", "minor", "note"}
    for case in review_cases:
        if not isinstance(case, dict):
            errors.append("review-evals 存在非对象 case")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append("review case 缺少 id")
            continue
        if case_id in seen_review:
            errors.append(f"review case ID 重复：{case_id}")
        seen_review.add(case_id)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{case_id}: prompt 不能为空")
        expected = case.get("expected_rule_ids")
        if not isinstance(expected, list):
            errors.append(f"{case_id}: expected_rule_ids 必须为数组")
        else:
            for rule_id in expected:
                if rule_id not in rule_ids:
                    errors.append(f"{case_id}: 未知规则 ID {rule_id}")
        forbidden = case.get("forbidden_claims")
        if not isinstance(forbidden, list) or not forbidden:
            errors.append(f"{case_id}: forbidden_claims 必须为非空数组")
        required = case.get("required_sections")
        if not isinstance(required, list) or not required:
            errors.append(f"{case_id}: required_sections 必须为非空数组")
        if case.get("expected_min_severity") not in severities:
            errors.append(f"{case_id}: expected_min_severity 非法")
        fixture = case.get("fixture")
        if fixture is not None:
            if not isinstance(fixture, str):
                errors.append(f"{case_id}: fixture 必须是字符串")
            else:
                fixture_path = (repo_root / fixture).resolve()
                try:
                    fixture_path.relative_to(repo_root.resolve())
                except ValueError:
                    errors.append(f"{case_id}: fixture 越出仓库：{fixture}")
                else:
                    if not fixture_path.exists():
                        errors.append(f"{case_id}: fixture 不存在：{fixture}")

    if len(review_cases) < 10:
        errors.append(f"Review Eval 不足：{len(review_cases)}，至少 10")

    return EvalValidationResult(len(trigger_cases), positive, negative, len(review_cases), errors)


def validate_skill_routing(repo_root: Path) -> tuple[int, list[str]]:
    """校验 skill-routing-evals.json（Skill 间路由消歧测试集）。"""
    path = repo_root / "evals" / "skill-routing-evals.json"
    errors: list[str] = []
    if not path.exists():
        return 0, [f"缺少文件：{path}"]
    try:
        data = load_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return 0, [f"读取 skill-routing 失败：{exc}"]

    skills = set(data.get("skills", [])) if isinstance(data, dict) else set()
    if not skills:
        errors.append("skill-routing：缺少 skills 列表")
    cases = data.get("cases", []) if isinstance(data, dict) else []
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            errors.append("skill-routing 存在非对象 case")
            continue
        cid = case.get("id")
        if not isinstance(cid, str) or not cid:
            errors.append("skill-routing case 缺少 id")
            continue
        if cid in seen:
            errors.append(f"skill-routing case ID 重复：{cid}")
        seen.add(cid)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{cid}: prompt 不能为空")
        if case.get("expected_primary") not in skills:
            errors.append(f"{cid}: expected_primary={case.get('expected_primary')} 不在 skills 列表")
        acceptable = case.get("acceptable")
        if not isinstance(acceptable, list):
            errors.append(f"{cid}: acceptable 必须为数组")
        else:
            for name in acceptable:
                if name not in skills:
                    errors.append(f"{cid}: acceptable 含非法 skill：{name}")
        if not isinstance(case.get("reason"), str) or not case["reason"].strip():
            errors.append(f"{cid}: reason 不能为空")
        if not isinstance(case.get("tags"), list) or not case["tags"]:
            errors.append(f"{cid}: tags 必须为非空数组")
    if len(cases) < 5:
        errors.append(f"skill-routing 案例过少：{len(cases)}，至少 5")
    return len(cases), errors


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 HarmonyOS-Design Eval")
    parser.add_argument("repo", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = validate_evals(args.repo.resolve())
    if result.errors:
        print("Eval 校验失败：")
        for error in result.errors:
            print(f"- {error}")
        return 1
    print(
        f"Eval 校验通过：触发 {result.trigger_count} 条（正 {result.positive_count}/负 {result.negative_count}），Review {result.review_count} 条。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
