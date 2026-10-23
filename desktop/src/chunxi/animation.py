from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter


@dataclass(frozen=True)
class Clip:
    frames: tuple[QImage, ...]
    durations_ms: tuple[int, ...]
    loop: bool = True

    def frame_at(self, elapsed_ms: float) -> QImage:
        duration = sum(self.durations_ms)
        cursor = elapsed_ms % duration if self.loop else min(elapsed_ms, duration - 0.001)
        for frame, hold in zip(self.frames, self.durations_ms):
            if cursor < hold:
                return frame
            cursor -= hold
        return self.frames[-1]


class SpriteLibrary:
    """Crop approved cells verbatim; never interpolate or redraw the character."""
    def __init__(self, manifest: Path):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        sources = {}
        for name, relative in data["sources"].items():
            image = QImage(str((manifest.parent / relative).resolve()))
            if image.isNull():
                raise ValueError(f"Cannot load sprite source: {relative}")
            sources[name] = image
        self.clips = {}
        for name, info in data["clips"].items():
            frames = []
            for source, row, column in info["cells"]:
                image = sources[source]
                x, y = column * 192, row * 208
                if x < 0 or y < 0 or x+192 > image.width() or y+208 > image.height():
                    raise ValueError(f"Out-of-bounds frame in {name}")
                frame = image.copy(x, y, 192, 208)
                registration = data.get("registration", {}).get(source)
                if registration:
                    scale = registration["scale"]
                    scaled = frame.scaled(round(192*scale), round(208*scale), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.FastTransformation)
                    canvas = QImage(192, 208, QImage.Format.Format_ARGB32_Premultiplied)
                    canvas.fill(Qt.GlobalColor.transparent)
                    painter = QPainter(canvas)
                    painter.drawImage(registration["x"], registration["y"], scaled)
                    painter.end()
                    frame = canvas
                frames.append(frame)
            holds = tuple(info["durations_ms"])
            if len(frames) != len(holds) or not holds or min(holds) <= 0:
                raise ValueError(f"Invalid animation: {name}")
            self.clips[name] = Clip(tuple(frames), holds, info.get("loop", True))

    def get(self, key: str, direction: int = 0) -> Clip:
        return self.clips[f"look-{direction:02}" if key == "look" else key]


class Animator:
    def __init__(self, library: SpriteLibrary, now: float):
        self.library = library
        self.key, self.direction, self.started = "breathing", 0, now

    def select(self, key: str, direction: int, now: float) -> bool:
        if (key, direction if key == "look" else 0) == (self.key, self.direction):
            return False
        self.key = key
        self.direction = direction if key == "look" else 0
        self.started = now
        return True

    def frame(self, now: float) -> QImage:
        return self.library.get(self.key, self.direction).frame_at((now-self.started)*1000)
