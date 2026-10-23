from __future__ import annotations

import ctypes
import math
import sys
from ctypes import wintypes

from PySide6.QtCore import QPoint
from PySide6.QtGui import QCursor


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]


class ActivityMonitor:
    """Poll input timestamps only; never capture keys, clicks or typed content."""
    def __init__(self, threshold: int = 3):
        self.threshold = threshold
        self.cursor = QCursor.pos()
        self.user32 = ctypes.WinDLL("user32", use_last_error=True) if sys.platform == "win32" else None
        if self.user32:
            self.user32.GetLastInputInfo.argtypes = [ctypes.POINTER(LASTINPUTINFO)]
            self.user32.GetLastInputInfo.restype = wintypes.BOOL
        self.stamp = self._stamp()

    def _stamp(self):
        if self.user32 is None:
            return None
        info = LASTINPUTINFO(ctypes.sizeof(LASTINPUTINFO), 0)
        return info.dwTime if self.user32.GetLastInputInfo(ctypes.byref(info)) else None

    def poll(self) -> tuple[bool, QPoint]:
        position, stamp = QCursor.pos(), self._stamp()
        moved = (position-self.cursor).manhattanLength() >= self.threshold
        active = moved or (stamp is not None and self.stamp is not None and stamp != self.stamp)
        if moved:
            self.cursor = position
        self.stamp = stamp
        return active, position


def direction_for(cursor: QPoint, center: QPoint) -> int:
    dx, dy = cursor.x()-center.x(), cursor.y()-center.y()
    # Original atlas convention: 0=up, 4=right, 8=down, 12=left.
    return int((math.degrees(math.atan2(dx, -dy)) + 360 + 11.25) // 22.5) % 16


class DragGesture:
    def __init__(self, threshold: int):
        self.threshold = threshold
        self.origin: QPoint | None = None
        self.window_origin = QPoint()
        self.dragging = False

    def press(self, point: QPoint, window_position: QPoint):
        self.origin, self.window_origin = point, window_position
        self.dragging = False

    def move(self, point: QPoint) -> QPoint | None:
        if self.origin is None:
            return None
        delta = point-self.origin
        if delta.manhattanLength() >= self.threshold:
            self.dragging = True
        return self.window_origin+delta if self.dragging else None

    def release(self) -> bool:
        was_dragging = self.dragging
        self.origin, self.dragging = None, False
        return was_dragging
