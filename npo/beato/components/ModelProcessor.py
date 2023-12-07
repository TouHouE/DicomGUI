try:
    import torch
except ModuleNotFoundError:
    print('Please install torch package.')
from PyQt6.QtCore import QThread, pyqtSignal, QObject
# from PyQt6.QtCore import

from wu_junde import utils as WUtils
from npo.beato import utils as BUtils
from npo.beato.data.emit import EmitData

class ModelProcessor(QThread):
    EmbeddingEvent = pyqtSignal()
    MaskEvent = pyqtSignal(EmitData)
    def __init__(self, root=None, weight_path=None, device=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # QThread.__init__(self)
        self.root = root
        self.model = None
        self.img_emb = None

        self.__thread_name = 'model_process'


        self.pause_flag = True
        self.model_update_flag = False
        self.image_embedding_update_flag = False
        self.decode_flag = False
        self.is_init = True
        self.moveToThread(self)

    def run(self):
        # if self.is_init:
        print(f'Sub thread:{self.__thread_name}> Model Thread Start.')
            # self.is_init = False

        while True:
            # print(f'path: {self.m}')
            self.update_model()
            self.update_image_embedding()

    #  TODO Complete mask decode part.
    #  TODO: Clear the try ... except ...

    def decode_mask(self, batch_prompt):
        if not self.model_update_flag or self.img_emb is None:
            return

        try:
            point_emb, mask_emb = self.model.prompt_encoder(**batch_prompt)
        except Exception as e:
            print(f'prompt_encoder: {e}')
        try:
            mask = self.model.mask_decoder(
                image_embeedings=self.img_emb,
                image_pe=self.model.prompt_encoder.get_dense_pe(),
                spare_prompt_embeddings=point_emb,
                dense_prompt_embeddings=mask_emb,
                multimask_output=False
            )
        except Exception as e:
            print(f'mask_decoder: {e}')

        self.MaskEvent.emit(EmitData({
            'mask': mask,
            'size': self.root.dicom_image.shape[1:]
        }))

    def update_image_embedding(self):
        if not self.image_embedding_update_flag and self.root.dicom_image is not None:
            return
        print(f'Extracting image embedding...')
        try:
            current_frame = self.root.dicom_image[int(self.root.frame_idx)]
            emb = self.model.image_encoder(BUtils.preprocessor(current_frame))
            self.img_emb = emb
            self.image_embedding_update_flag = False
            print(f'Done')
            self.EmbeddingEvent.emit()
        except Exception as e:
            print(e)
    def update_model(self):
        # case_model_init = self.model is None and self.root.weight_path is not None
        if self.model_update_flag:
            print(f'Model Loading...')
            try:
                self.model = BUtils.load_nn_model(self.root.weight_path, self.root.device).to(self.root.device)
                self.model.eval()
                self.model_update_flag = False
                self.image_embedding_update_flag = True
            except Exception as e:
                print(e)

    @property
    def thread_name(self):
        return self.__thread_name

    @thread_name.setter
    def thread_name(self, thread_name):
        self.__thread_name = thread_name

    def is_work(self):
        return self.model is not None and self.img_emb is not None
