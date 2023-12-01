import icecream
from PyQt6.QtWidgets import QWidget, QLabel, QFileDialog, QComboBox, QPushButton, QHBoxLayout
from npo.beato import utils as BUtils


class Declarator(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weight_select_btn = QPushButton("model", self)
        self.device_hint = QLabel("Device: ", self)
        self.current_device = QComboBox(self)

        self.weight_select_btn.setObjectName('weight_select_btn')
        self.device_hint.setObjectName('device_hint')
        self.current_device.setObjectName('current_device')

        self._init_layout()

    def _init_layout(self):
        grid = QHBoxLayout(self)
        grid.addWidget(self.weight_select_btn)
        grid.addWidget(self.device_hint)
        grid.addWidget(self.current_device)
        self.setLayout(grid)


class AlgorithmSelectUIPanel(Declarator):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.weight_select_btn.clicked.connect(self.clicked_weight_select_btn)
        self.update_device_list()
        self.current_device.currentIndexChanged.connect(self.indexChanged_current_device)

    def indexChanged_current_device(self):
        new_device = icecream.ic(self.current_device.currentText())
        self.root.update_device(new_device)
        self.root.update_title()

    def clicked_weight_select_btn(self):
        file, _ = QFileDialog.getOpenFileName()
        self.root.set_weight_path(file)
        self.root.update_title()
        self.root.update_model_path(file)

    def update_device_list(self):
        self.current_device.clear()
        self.current_device.addItems(BUtils.get_device_list())
        self.root.update_device(self.current_device.currentText())
        self.root.update_title()

