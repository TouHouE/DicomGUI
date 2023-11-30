from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton
# from npo.beato.window.MainApp import MainApp


class Declarator(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt_ww = QLabel('WW', self)
        self.prompt_wl = QLabel("WL", self)
        self.ww_input = QLineEdit(parent=self)
        self.wl_input = QLineEdit(parent=self)
        self.confirm_btn = QPushButton("Confirm", parent=self)
        self._init_layout()

    def _init_layout(self):
        pixel_range_layout = QHBoxLayout(self)

        pixel_range_layout.addWidget(self.prompt_ww)
        pixel_range_layout.addWidget(self.ww_input)
        pixel_range_layout.addWidget(self.prompt_wl)
        pixel_range_layout.addWidget(self.wl_input)
        pixel_range_layout.addWidget(self.confirm_btn)


class WindowRangeUIPanel(Declarator):
    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(*args, **kwargs)
        self.confirm_btn.clicked.connect(self.update_pixel_range)

    def update_pixel_range(self):
        ww = self.ww_input.text()
        wl = self.wl_input.text()

        if ww.isdigit() and wl.isdigit():
            ww, wl = int(ww), int(wl)
        else:
            return
        self.root.ww_wl = [ww, wl]
        self.root.main_panel.dicom_viewer.plot_dicom(ww, wl)

    def set_ww(self, ww):
        self.ww_input.setText(f'{ww}')

    def set_wl(self, wl):
        self.wl_input.setText(f'{wl}')
