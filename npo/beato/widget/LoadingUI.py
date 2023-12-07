from PyQt6.QtWidgets import QDialog, QProgressBar, QHBoxLayout


class LoadingUI(QDialog):
    def __init__(self, info):
        super().__init__()
        self.setWindowTitle(info)
        self.progress = QProgressBar(self)
        self.progress.setTextVisible(False)
        # self.layout().addWidget(self.progress)
        lout = QHBoxLayout()
        lout.addWidget(self.progress)
        self.setLayout(lout)