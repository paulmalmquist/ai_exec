from __future__ import annotations

from pathlib import Path

from app.core.config import get_settings
from app.core.config import load_yaml

POLICY_TEMPLATE = {
    "channels": [
        {"channel": "public", "requires_approval": True},
        {"channel": "external", "requires_approval": True},
        {"channel": "internal", "requires_approval": False},
    ]
}


def main() -> None:
    settings = get_settings()
    path = settings.policy_path
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("channels:\n  - channel: public\n    requires_approval: true\n", encoding="utf-8")
        print(f"Created policy file at {path}")
    else:
        print(f"Policy already exists at {path}")


if __name__ == "__main__":
    main()
