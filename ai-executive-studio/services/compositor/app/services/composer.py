from __future__ import annotations

from pathlib import Path

import structlog

logger = structlog.get_logger()


class Composer:
    def compose(self, foreground: Path, background: Path | None, captions: Path | None, theme: str | None) -> Path:
        output = Path("/tmp/composite.mp4")
        output.write_bytes(b"FAKECOMPOSITE")
        logger.info(
            "compositor.compose",
            foreground=str(foreground),
            background=str(background),
            captions=str(captions),
            theme=theme,
        )
        return output


composer = Composer()
