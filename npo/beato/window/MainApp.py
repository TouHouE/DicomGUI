from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QMainWindow, QStatusBar
import pydicom as pyd
import numpy as np

from npo.beato.components.ModelProcessor import ModelProcessor
from npo.beato.widget import MainPanel, TopMenuBar
from npo.beato import utils as BUtils
from npo.beato import constant as BU

from typing import List, Union


class Attribute:
    def __init__(self):
        self.dicom_file = None
        self.dicom_image = None
        self.ww_wl = None
        self.frame_idx: BUtils.LimitNumber = BUtils.LimitNumber(0, 1)
        self.prompt_mode = BU.PromptType.DEFAULT
        self.path_list = []

        self.device = None
        self.weight_path = None


    def set_device(self, v: str):
        self.device = v

    def set_weight_path(self, v: str):
        self.weight_path = v

    def set_dicom_file(self, v: pyd.FileDataset):
        self.dicom_file = v

    def set_ww_wl(self, v: List[int]):
        self.ww_wl = v

    def set_frame_idx(self, v: BUtils.LimitNumber):
        self.frame_idx = v

    def set_prompt_mode(self, v: str):
        self.prompt_mode = v

    def set_path_list(self, v: List[str]):
        self.path_list = v

    def set_dicom_image(self, v: np.ndarray):
        self.dicom_image = v


class BuildUI(QMainWindow):
    def __init__(self, thread_, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('SegUI')
        self.model_worker = thread_
        self.model_worker.root = self

        self.main_panel = MainPanel(self, parent=self)
        self.menu_bar = TopMenuBar(self, parent=self)
        self.status_bar = QStatusBar(self)

        self.status_bar.setObjectName('status_bar')
        self.menu_bar.setObjectName('menu_bar')
        self.main_panel.setObjectName("main_panel")

        self.setCentralWidget(self.main_panel)
        self.setMenuBar(self.menu_bar)
        self.setStatusBar(self.status_bar)


class MainApp(BuildUI, Attribute):
    app_name: str = 'SegUI'

    def __init__(self, thread_, *args, **kwargs):
        super().__init__(thread_, *args, **kwargs)
        # self.model_thread = QThread(self)
        # self.model_worker = ModelProcessor(self, self.weight_path, self.device)
        # self.model_worker: ModelProcessor = thread_
        # self.model_worker.root = self
        # self.model_worker.moveToThread(self.model_thread)
        # self.model_worker.threa
        # self.model_worker.thread_name = self.model_thread.currentThreadId()
        # self.model_worker.start()

        # self.status_bar.setStatusTip('fda')
        # self.status_bar.showMessage('wtf')

    def show_cursor_info(self, x, y, value):
        frame = f'Images:{self.frame_idx}'
        pos = f'(X, Y, Value)=({x}, {y}, {value})'
        self.status_bar.showMessage(f'{frame} | {pos}')

    def update_title(self):
        self.setWindowTitle(f'SegUI - {self.weight_path} - {self.device}')

    def update_model_path(self, path):
        self.set_weight_path(path)
        # self.model_worker.update_path(path)
        self.model_worker.model_update_flag = True

    def update_device(self, device):
        self.set_device(device)
        # self.model_worker.update_device(device)
        self.model_worker.model_update_flag = True

    def update_frame_idx(self, idx):
        self.set_frame_idx(idx)
        self.model_worker.image_embedding_update_flag = True

    def set_title(self, info):
        self.setWindowTitle(f'SegUI - {info}')
