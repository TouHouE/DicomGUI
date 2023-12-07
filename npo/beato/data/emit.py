import numpy as np
from torchvision.transforms import transforms
import torch

class EmitData:
    def __init__(self, data):
        self.data = data

    def mask(self) -> np.ndarray:
        img = self.data['img']
        hw = self.data['size']
        img = img.squeeze(0)

        if torch.max(img) > 1 or torch.min(img) < 0:
            img = torch.sigmoid(img)
        img = transforms.Resize(hw)(img)
        return img.numpy().transpose((1, 2, 0))

    def __getitem__(self, item):
        return self.data[item]