from __future__ import annotations

import uuid
from pathlib import Path

import structlog

from ..core.config import get_settings

logger = structlog.get_logger()


class VoiceRegistry:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.speakers_dir = self.settings.speaker_config_dir
        self.speakers_dir.mkdir(parents=True, exist_ok=True)

    def register(self, name: str) -> str:
        speaker_id = str(uuid.uuid4())
        config_path = self.speakers_dir / f"{speaker_id}.yaml"
        config_path.write_text("seed: 42\nnoise_scale: 0.33\n", encoding="utf-8")
        logger.info("tts.voice.registered", speaker_id=speaker_id, name=name)
        return speaker_id

    def synthesize(self, speaker_id: str, text: str) -> tuple[Path, dict[str, float]]:
        audio_path = self.speakers_dir / f"{speaker_id}.wav"
        audio_path.write_bytes(b"RIFF....FAKEAUDIO")
        phonemes = {"tokens": ["AH", "IY"], "durations": [0.1, 0.2]}
        logger.info("tts.voice.synthesize", speaker_id=speaker_id, text=text)
        return audio_path, phonemes


registry = VoiceRegistry()
