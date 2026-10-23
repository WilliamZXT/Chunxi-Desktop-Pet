"""Window placement in Qt logical coordinates, including negative screen origins."""
from PySide6.QtCore import QPoint, QRect


def visible_position(position: QPoint, size, workareas: list[QRect]) -> QPoint:
    if not workareas:
        return position
    window = QRect(position, size)
    area = max(workareas, key=lambda rect: rect.intersected(window).width()*rect.intersected(window).height())
    if not area.intersects(window):
        center = window.center()
        area = min(workareas, key=lambda rect: (rect.center()-center).manhattanLength())
    x = max(area.left(), min(position.x(), area.right()-size.width()+1))
    y = max(area.top(), min(position.y(), area.bottom()-size.height()+1))
    return QPoint(x, y)
