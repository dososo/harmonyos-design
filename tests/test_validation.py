from pathlib import Path

import yaml

from scripts.validate_evals import validate_evals
from scripts.validate_rules import validate_rules
from scripts.validate_skills import validate_skills

ROOT = Path(__file__).resolve().parents[1]


def load_rules() -> list[dict]:
    data = yaml.safe_load((ROOT / "rules" / "harmony-design-rules.yaml").read_text(encoding="utf-8"))
    return data["rules"]


def test_skills_validate() -> None:
    result = validate_skills(ROOT)
    assert result.errors == []
    assert result.skill_count == 3


def test_rules_validate() -> None:
    result = validate_rules(ROOT)
    assert result.errors == []
    assert result.rule_count == 38
    assert result.source_count >= 30


def test_evals_validate() -> None:
    result = validate_evals(ROOT)
    assert result.errors == []
    assert result.positive_count >= 25
    assert result.negative_count >= 25
    assert result.review_count >= 15


def test_comment_and_second_thread_rules_exist() -> None:
    ids = {rule["id"] for rule in load_rules()}
    assert {
        "HD-ASYNC-001",
        "HD-ASYNC-004",
        "HD-FOUNDATION-004",
        "HD-FOUNDATION-005",
        "HD-FOUNDATION-006",
        "HD-FOUNDATION-007",
    }.issubset(ids)


def test_every_rule_has_knowledge_layer() -> None:
    rules = load_rules()
    assert all(rule["stability"] in {"evergreen", "versioned", "experimental"} for rule in rules)
    assert all(rule["design_layer"] in {"foundation", "platform", "project"} for rule in rules)


def test_platform_rules_are_versioned() -> None:
    for rule in load_rules():
        if rule["design_layer"] == "platform":
            assert rule["stability"] == "versioned"


def test_autofix_is_disabled() -> None:
    assert all(rule["autofix"]["enabled"] is False for rule in load_rules())


def test_skill_routing_validate() -> None:
    from scripts.validate_evals import validate_skill_routing

    count, errors = validate_skill_routing(ROOT)
    assert errors == []
    assert count >= 5


def test_internal_links_valid() -> None:
    from scripts.check_links import check_links

    assert check_links(ROOT) == []
