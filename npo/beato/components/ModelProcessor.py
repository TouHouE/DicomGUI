import torch
from PyQt6.QtCore import QThread, pyqtSignal
# from PyQt6.QtCore import

from wu_junde import utils as WUtils
from npo.beato import utils as BUtils
from npo.beato.data.emit import EmitData

class ModelProcessor(QThread):
    EmbeddingEvent = pyqtSignal(EmitData)
    MaskEvent = pyqtSignal(EmitData)
    def __init__(self, root, weight_path, device, *args, **kwargs):
        super().__init__(*args, **kwargs)
        QThread.__init__(self)
        self.root = root
        self.weight_path = weight_path
        self.device = device # ['cpu', 'cuda:0'...]
        self.model = None
        self.__thread_name = 'model_process'
        self.EmbeddingEvent.connect(self.root.update_image_emb)
        self.pause_flag = True

    def run(self):
        print(f'Model Thread Start.')

        while True:
            if self.model is None and self.weight_path is not None:
                print(f'Model Loading...')
                self.load_model()

            if self.pause_flag:
                continue
            else:
                print('Exit Pause')

    def image_encoder(self):
        # self.model.
        pass

    def load_model(self):
        self.model = BUtils.load_nn_model(self.weight_path, self.device)
    def udpate_path(self, path):
        self.weight_path = path

    def update_device(self, device):
        self.device = device