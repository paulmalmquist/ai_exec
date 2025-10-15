from __future__ import annotations

from pathlib import Path

import structlog

logger = structlog.get_logger()


class SadTalkerService:
    def animate(self, image: Path, audio: Path) -> Path:
        output = Path("/tmp/sadtalker-output.mp4")
        output.write_bytes(b"FAKEAVATAR")
        logger.info("sadtalker.animate", image=str(image), audio=str(audio))
        return output


service = SadTalkerService()
