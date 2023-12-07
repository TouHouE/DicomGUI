from PyQt6.QtCore import qDebug
from PyQt6.QtWidgets import QApplication
from npo.beato.window import MainApp
from npo.beato.components import ModelProcessor
import sys


def main():
    app = QApplication(sys.argv)
    model_worker = ModelProcessor()
    Handler = MainApp(model_worker)
    Handler.resize(1000, 600)
    # m_win = MainPanel(Handler)
    # Handler.setCentralWidget(m_win)
    Handler.model_worker.start()
    Handler.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()