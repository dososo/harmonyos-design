#!/usr/bin/env python3
"""校验机器可读规则、来源登记和跨引用。"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


@dataclass(frozen=True)
class RuleValidationResult:
    rule_count: int
    source_count: int
    errors: list[str]


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_rules(repo_root: Path) -> RuleValidationResult:
    rules_path = repo_root / "rules" / "harmony-design-rules.yaml"
    schema_path = repo_root / "rules" / "schema.json"
    sources_path = repo_root / "rules" / "sources.yaml"
    errors: list[str] = []

    for path in (rules_path, schema_path, sources_path):
        if not path.exists():
            errors.append(f"缺少文件：{path}")
    if errors:
        return RuleValidationResult(0, 0, errors)

    try:
        data = load_yaml(rules_path)
        sources_data = load_yaml(sources_path)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError, json.JSONDecodeError) as exc:
        return RuleValidationResult(0, 0, [f"读取规则文件失败：{exc}"])

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(x) for x in error.absolute_path) or "<root>"
        errors.append(f"规则 Schema 错误 {location}: {error.message}")

    rules = data.get("rules", []) if isinstance(data, dict) else []
    sources = sources_data.get("sources", []) if isinstance(sources_data, dict) else []
    source_map: dict[str, dict[str, Any]] = {}
    for source in sources:
        if not isinstance(source, dict):
            errors.append("sources.yaml 中存在非对象条目")
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str):
            errors.append("sources.yaml 中存在缺少字符串 id 的来源")
            continue
        if source_id in source_map:
            errors.append(f"来源 ID 重复：{source_id}")
        source_map[source_id] = source
        if source.get("tier") not in {"H1", "H2", "H3", "H4"}:
            errors.append(f"来源 {source_id} 的 tier 非法")
        if not source.get("title") or not source.get("organization") or not source.get("scope"):
            errors.append(f"来源 {source_id} 缺少 title、organization 或 scope")

    seen_ids: set[str] = set()
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        rule_id = rule.get("id")
        if not isinstance(rule_id, str):
            continue
        if rule_id in seen_ids:
            errors.append(f"规则 ID 重复：{rule_id}")
        seen_ids.add(rule_id)

        source = rule.get("source", {})
        source_id = source.get("id") if isinstance(source, dict) else None
        if source_id not in source_map:
            errors.append(f"规则 {rule_id} 引用了未登记来源：{source_id}")
        elif rule.get("source_tier") != source_map[source_id].get("tier"):
            errors.append(
                f"规则 {rule_id} 的 source_tier={rule.get('source_tier')} 与来源 {source_id} 的 tier={source_map[source_id].get('tier')} 不一致"
            )

        value_kind = rule.get("value_kind")
        has_values = "values" in rule
        if has_values and value_kind == "NONE":
            errors.append(f"规则 {rule_id} 包含 values，但 value_kind 为 NONE")
        if value_kind in {"OFFICIAL_REQUIREMENT", "OFFICIAL_REFERENCE", "ARKUI_DEFAULT", "OBSERVED", "HOUSE_STYLE"} and not has_values:
            errors.append(f"规则 {rule_id} 声明 value_kind={value_kind}，但未提供 values")

        autofix = rule.get("autofix", {})
        if isinstance(autofix, dict) and autofix.get("enabled") is not False:
            errors.append(f"规则 {rule_id}: 当前 Draft 必须关闭 autofix")

        if rule.get("source_tier") in {"H3", "H4"} and rule.get("normativity") == "MUST":
            # 允许项目治理类 MUST，但要求是 blocker/major 且来源措辞不能伪装官方。
            if rule.get("severity") not in {"blocker", "major"}:
                errors.append(f"规则 {rule_id}: H3/H4 的 MUST 必须有明确高影响理由")

        stability = rule.get("stability")
        design_layer = rule.get("design_layer")
        if stability == "experimental" and rule.get("normativity") == "MUST":
            errors.append(f"规则 {rule_id}: experimental 规则不得使用 MUST")
        if design_layer == "project" and rule.get("source_tier") != "H4":
            errors.append(f"规则 {rule_id}: project 层规则应使用 H4 来源")
        if design_layer == "platform" and stability == "evergreen":
            errors.append(f"规则 {rule_id}: platform 层规则不能标记为 evergreen")

    if len(rules) < 25:
        errors.append(f"规则数量不足：{len(rules)}，至少需要 25")
    if len(rules) > 60:
        errors.append(f"当前 Draft 种子规则过多：{len(rules)}，建议先控制在 60 以内")

    return RuleValidationResult(len(rules), len(source_map), errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 HarmonyOS-Design 规则库")
    parser.add_argument("repo", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = validate_rules(args.repo.resolve())
    if result.errors:
        print("规则校验失败：")
        for error in result.errors:
            print(f"- {error}")
        return 1
    print(f"规则校验通过：{result.rule_count} 条规则，{result.source_count} 个来源。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
