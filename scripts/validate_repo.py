#!/usr/bin/env python3
"""一键执行 HarmonyOS-Design 全仓库离线校验。"""

from __future__ import annotations

import argparse
from pathlib import Path

from validate_evals import validate_evals, validate_skill_routing
from validate_rules import validate_rules
from validate_skills import validate_skills


def main() -> int:
    parser = argparse.ArgumentParser(description="一键校验 HarmonyOS-Design 仓库")
    parser.add_argument("repo", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.repo.resolve()

    skill_result = validate_skills(root)
    rule_result = validate_rules(root)
    eval_result = validate_evals(root)
    routing_count, routing_errors = validate_skill_routing(root)

    errors = [*skill_result.errors, *rule_result.errors, *eval_result.errors, *routing_errors]
    if errors:
        print("仓库校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print("仓库校验通过。")
    print(f"- Skill：{skill_result.skill_count}")
    print(f"- 规则：{rule_result.rule_count}")
    print(f"- 来源：{rule_result.source_count}")
    print(f"- Trigger Eval：{eval_result.trigger_count}（正 {eval_result.positive_count}/负 {eval_result.negative_count}）")
    print(f"- Review Eval：{eval_result.review_count}")
    print(f"- Skill 路由 Eval：{routing_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
