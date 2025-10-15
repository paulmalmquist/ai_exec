from __future__ import annotations

import structlog

from ..core.config import get_settings, load_yaml
from ..models.schemas import PolicyRule

logger = structlog.get_logger()


def load_policy_rules() -> list[PolicyRule]:
    data = load_yaml(get_settings().policy_path)
    rules: list[PolicyRule] = []
    for item in data.get("channels", []):
        rules.append(PolicyRule(**item))
    logger.info("policy.rules.loaded", count=len(rules))
    return rules


def requires_approval(channel: str | None, rules: list[PolicyRule]) -> bool:
    if not channel:
        return False
    for rule in rules:
        if rule.channel == channel:
            return rule.requires_approval
    return False
