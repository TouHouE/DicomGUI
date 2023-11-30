from PyQt6.QtWidgets import QWidget, QLabel, QTableView, QVBoxLayout
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from npo.beato import utils as BUtils

class Declarator(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.prompt_image_idx = QLabel('Images:/', self)

        self.prompt_image_pixel = QLabel('Cursor(X, Y, Value):', self)

        self._init_layout()

    def _init_layout(self):
        grid = QVBoxLayout()
        grid.addWidget(self.prompt_image_idx)
        grid.addWidget(self.prompt_image_pixel)
        self.setLayout(grid)


class ImageInfoFocus(Declarator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def change_image_idx(self, text: BUtils.LimitNumber):
        self.prompt_image_idx.setText(f'Images:{text}')

    def change_pixel(self, x, y, value):
        value = '-' if value is None else value

        self.prompt_image_pixel.setText(f'Cursor(X, Y, Value):({x}, {y}, {value})')