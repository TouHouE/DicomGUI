from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QAbstractItemView

from npo.beato.widget import AlgorithmSelectUIPanel, CursorTypeUIPanel, WindowRangeUIPanel
from npo.beato.components import DicomFileItem
from npo.beato import utils as BUtils

from typing import List
from icecream import ic


class Declarator(QWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_panel = AlgorithmSelectUIPanel(root, parent=self)
        self.cursor_panel = CursorTypeUIPanel(root, parent=self)
        self.window_range_panel = WindowRangeUIPanel(root, parent=self)
        self.file_ui = QTreeWidget(self)

        self.file_ui.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.model_panel.setObjectName('model_panel')
        self.cursor_panel.setObjectName('cursor_panel')
        self.window_range_panel.setObjectName('window_range_panel')
        self.file_ui.setObjectName('file_ui')

        self._init_layout()

    def _init_layout(self):
        grid = QVBoxLayout(self)
        grid.addWidget(self.model_panel)
        grid.addWidget(self.window_range_panel)
        grid.addWidget(self.cursor_panel)
        grid.addWidget(self.file_ui)
        self.setLayout(grid)


class ToolPanel(Declarator):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.file_ui.itemClicked.connect(self.itemClicked_file_ui)

    def itemClicked_file_ui(self, item: DicomFileItem):
        if item.childCount() > 0:
            return
        dfile = BUtils.read_dicom(item.get_path())
        ww_wl = BUtils.get_default_ww_wl(dfile)

        try:
            self.root.set_dicom_file(dfile)
            self.root.set_dicom_image(dfile.pixel_array)
            self.root.set_ww_wl(ww_wl)
            self.root.set_frame_idx(BUtils.LimitNumber(0, int(dfile.NumberOfFrames)))
            self.root.main_panel.dicom_viewer.plot_dicom(*ww_wl)

            self.window_range_panel.set_ww(ww_wl[0])
            self.window_range_panel.set_wl(ww_wl[1])
        except Exception as e:
            print(e)

    def add_list(self, new_path_list: List[str]):
        self.file_ui.clear()
        self.root.path_list.extend(new_path_list)

        for idx, path in enumerate(self.root.path_list):
            file_item = DicomFileItem(path)
            self.file_ui.insertTopLevelItem(idx, file_item)

    def update_list(self, new_path_list: List[str]):
        self.file_ui.clear()
        new_path_list = BUtils.handle_path_input(new_path_list)
        self.root.set_path_list(new_path_list)
        container = []

        for idx, path in enumerate(self.root.path_list):
            file_item = DicomFileItem(path)
            self.file_ui.insertTopLevelItem(idx, file_item)

        #
        # for key, value in arg.items():
        #     folder_item = QTreeI([key])
        #
        #     for v in value:
        #         file_item = DicomFileItem([v])
        #         folder_item.addChild(file_item)
        #     container.append(folder_item)
        # self.document_list.insertTopLevelItems(0, container)