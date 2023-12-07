from npo.beato import utils as BU
import pydicom as pyd
import torch
import numpy as np
from torchvision.transforms import transforms

transfer = transforms.Compose([
    # transforms.Resize((1024, 1024)),
    transforms.ToTensor()
])
device = 'cpu'
model = BU.load_nn_model('./static/weight/Model', device)
model = model.to(device)
df = pyd.read_file('./0002.DCM')
dimgs_np = 255 - df.pixel_array  # SxHxW
dimg_np = dimgs_np[25]  #HxW
dimg_np = dimg_np[:, :, None] #HxWx1
# print(dimg_np.shape)
dimg_np = np.repeat(dimg_np, 3, 2) #HxWx3
# print(dimg_np.shape)
print(f'The original image shape: ({dimg_np.shape}')

dimg_pt = transfer(np.resize(dimg_np, (1024, 1024, 3)))
prompt_point = torch.as_tensor([[251, 51]], dtype=torch.float) # Nx2
prompt_label = torch.as_tensor([1], dtype=torch.int) # Nx1
click_prompt = (prompt_point[None, :, :].to(device), prompt_label[None, :].to(device))
box_prompt = torch.as_tensor([157, 137, 181, 174], dtype=torch.float)# 4

emb_img = model.image_encoder(dimg_pt.to(device).unsqueeze(0))
embs, embd = emb_prompt = model.prompt_encoder(
    points=click_prompt,
    # boxes=box_prompt[None, :], #Nx4
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

# msa_predict = model([
#     {'image':  - dimg_pt.to(device),
#      'original_size': (512, 512),
#      # 'boxes': box_prompt.unsqueeze(0),
#      'point_coords': prompt_point.unsqueeze(0),
#      'point_labels': prompt_label.unsqueeze(0)
#      }
# ], False)[0]
# pred_masks = msa_predict['masks']

print(pred_masks.shape)

# plt.imshow(dimg_np.transpose((1, 2, 0)))

import torchvision

if torch.max(pred_masks) > 1 or torch.min(pred_masks) < 0:
    pred_masks = torch.sigmoid(pred_masks)
pred_masks = transforms.Resize((512, 512))(pred_masks)
import matplotlib.pyplot as plt

with torch.no_grad():
    plt.imshow(dimg_np)
    plt.imshow(pred_masks.squeeze(0)[0].squeeze(0).numpy(), alpha=.5)
    plt.scatter(*prompt_point.numpy()[0])
    plt.show()