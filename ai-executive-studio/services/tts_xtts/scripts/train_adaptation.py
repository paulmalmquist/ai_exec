#!/usr/bin/env python
"""Few-shot voice adaptation script.

Usage::
    poetry run python scripts/train_adaptation.py --samples ./samples --output ./checkpoints

This script documents the steps required to run Coqui XTTS v2 speaker adaptation. GPU with 16GB VRAM recommended.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def run(samples: Path, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    print(f"Preparing adaptation from {samples} → {output}")
    print("Download pretrained XTTS weights if not present (see README).")
    print("Launch training with GPUs: python -m trainer --gpus 1 --config configs/xtts-adapt.yaml")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XTTS adaptation helper")
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.samples, args.output)
