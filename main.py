from PyQt6.QtCore import qDebug
from PyQt6.QtWidgets import QApplication
from npo.beato.window import MainApp
import sys


def main():
    app = QApplication(sys.argv)
    Handler = MainApp()
    Handler.resize(1000, 600)
    # m_win = MainPanel(Handler)
    # Handler.setCentralWidget(m_win)

    Handler.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()