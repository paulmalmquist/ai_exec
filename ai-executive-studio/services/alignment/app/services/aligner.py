from __future__ import annotations

from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger()


class MFAService:
    def __init__(self) -> None:
        self.available = True

    def align(self, transcript: str, wav_path: Path) -> dict[str, Any]:
        if not self.available:
            logger.warning("mfa.unavailable", transcript_length=len(transcript))
            return {
                "tokens": transcript.split(),
                "timestamps": [index * 0.3 for index, _ in enumerate(transcript.split())],
            }
        logger.info("mfa.align", wav=str(wav_path))
        return {
            "tokens": ["AH", "IY"],
            "timestamps": [0.0, 0.15, 0.36],
        }


aligner = MFAService()
