from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsEllipseItem
import typing


class ClickPromptItem(QGraphicsEllipseItem):
    def __init__(self, init_point, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_p = init_point

    def mousePressEvent(self, event: typing.Optional['QGraphicsSceneMouseEvent']) -> None:
        pass

    def mouseReleaseEvent(self, event: typing.Optional['QGraphicsSceneMouseEvent']) -> None:
        if self.init_p !=