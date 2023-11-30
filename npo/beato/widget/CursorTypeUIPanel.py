import icecream
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QIcon

from npo.beato import constant as BC


class Declarator(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.click_btn = QPushButton('Click', self)
        self.click_btn.setObjectName("click_btn")

        self.box_btn = QPushButton('Box', self)
        self.box_btn.setObjectName("box_btn")

        self.doodle_btn = QPushButton('Brush', self)
        self.doodle_btn.setObjectName('doodle_btn')

        self.mask_btn = QPushButton('Mask', self)
        self.mask_btn.setObjectName('mask_btn')

        self.default_btn = QPushButton('Mouse', self)
        self.default_btn.setObjectName('default_btn')

        self._init_grid()

    def _init_grid(self):
        grid = QHBoxLayout(self)
        grid.setObjectName("QHBoxLayout_1")
        grid.addWidget(self.click_btn)
        grid.addWidget(self.box_btn)
        grid.addWidget(self.doodle_btn)
        grid.addWidget(self.mask_btn)
        grid.addWidget(self.default_btn)
        self.setLayout(grid)


class CursorTypeUIPanel(Declarator):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.click_btn.clicked.connect(lambda x: self.clicked_prompt_btn(x, self.click_btn))
        self.box_btn.clicked.connect(lambda x: self.clicked_prompt_btn(x, self.box_btn))
        self.doodle_btn.clicked.connect(lambda x: self.clicked_prompt_btn(x, self.doodle_btn))
        self.mask_btn.clicked.connect(lambda x: self.clicked_prompt_btn(x, self.mask_btn))
        self.default_btn.clicked.connect(lambda x: self.clicked_prompt_btn(x, self.default_btn))

    def clicked_prompt_btn(self, _, btn: QPushButton):
        mode = btn.text().lower()
        self.root.prompt_mode = icecream.ic(BC.PromptType(mode))
        self.root.status_bar.showMessage(f'Click: {mode}')

