import pydicom as pyd
from PyQt6.QtWidgets import QPushButton, QLabel, QFileDialog, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QTreeWidget, QTreeWidgetItem, QAbstractItemView

from typing import List, Union
from PyQt6.QtCore import QRect

from npo.beato.widget import (
    DicomGraphicViewer, ToolPanel
)
from npo.beato.components import (
    DicomFileItem
)
# from npo.beato.widget.ImageFocusInfo import ImageInfoFocus
from npo.beato import utils as BUtils


class Declarator(QWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tool_panel = ToolPanel(root, parent=self)
        self.dicom_viewer = DicomGraphicViewer(root, parent=self)

        self.tool_panel.setMaximumWidth(300)

        self.tool_panel.setObjectName("tool_panel")
        self.dicom_viewer.setObjectName("dicom_viewer")

        self._init_layout()

    def _init_layout(self):
        grid = QHBoxLayout(self)
        grid.addWidget(self.tool_panel)
        grid.addWidget(self.dicom_viewer)

        self.setLayout(grid)


class MainPanel(Declarator):

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root


    # For object pixel_update_btn
    def update_list(self, new_path_list: List[str]):
        self.document_list.clear()
        self.path_list = new_path_list
        arg = BUtils.handle_path_input(new_path_list)
        container = []
        # cnt = 0

        for key, value in arg.items():
            folder_item = QTreeWidgetItem([key])

            for v in value:
                file_item = QTreeWidgetItem([v])
                folder_item.addChild(file_item)
            container.append(folder_item)
        self.document_list.insertTopLevelItems(0, container)
        # return container[0]
