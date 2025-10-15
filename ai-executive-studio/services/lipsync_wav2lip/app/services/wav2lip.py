from __future__ import annotations

from pathlib import Path
from typing import Optional

import structlog

logger = structlog.get_logger()


class Wav2LipService:
    def sync(self, audio_path: Path, video_path: Optional[Path] = None, image_path: Optional[Path] = None) -> Path:
        output = Path("/tmp/wav2lip-output.mp4")
        output.write_bytes(b"FAKEVIDEO")
        logger.info("wav2lip.sync", audio=str(audio_path), video=str(video_path), image=str(image_path))
        return output


service = Wav2LipService()
