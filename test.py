from npo.beato import utils as BU
import pydicom as pyd
import torch
import numpy as np
from torchvision.transforms import transforms

transfer = transforms.Compose([
    # transforms.Resize((1024, 1024)),
    transforms.ToTensor()
])

model = BU.load_nn_model('./static/weight/Model', 0)
df = pyd.read_file('./0002.DCM')
dimgs_np = df.pixel_array  # SHW
dimg_np = dimgs_np[0]  #HW
dimg_np = dimg_np[:, None] #HW1
print(dimg_np.shape)
dimg_np = np.repeat(dimg_np, 3, 2) #HW3
print(dimg_np.shape)

dimg_pt = transfer(np.resize(dimg_np, (1024, 1024, 3)))
prompt_point = torch.as_tensor([[281, 51]], dtype=torch.float)
prompt_label = torch.as_tensor([1], dtype=torch.int)
click_prompt = (prompt_point[None, :, :].to('cuda:0'), prompt_label[None, :].to('cuda:0'))
emb_img = model.image_encoder(dimg_pt.to('cuda:0').unsqueeze(0))
embs, embd = emb_prompt = model.prompt_encoder(
    points=click_prompt,
    boxes=None,
    masks=None
)

pred_masks, _ = model.mask_decoder(
    image_embeddings=emb_img,
    image_pe=model.prompt_encoder.get_dense_pe(),
    sparse_prompt_embeddings=embs,
    dense_prompt_embeddings=embd,
    multimask_output=False
)

print(pred_masks.shape)

# plt.imshow(dimg_np.transpose((1, 2, 0)))

import torchvision

if torch.max(pred_masks) > 1 or torch.min(pred_masks) < 0:
    pred_masks = torch.sigmoid(pred_masks)

import matplotlib.pyplot as plt

plt.imshow(dimg_np)
plt.imshow(pred_masks[0], alpha=.75)
plt.show()