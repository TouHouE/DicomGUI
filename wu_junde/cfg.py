import argparse

class Arg:
    def __init__(self):
        self.net = 'sam'
        self.baseline = 'unet'
        self.set_net = 'transunet'
        self.mod = ''
        self.type = 'map'
        self.vis = None
        self.reverse = False
        self.pretrain = False
        self.val_freq = 100
        self.gpu = True
        self.gpu_device = 0
        self.sim_gpu = 0
        self.epoch_ini = 1
        self.image_size = 256
        self.out_size = 256
        self.patch_size = 2
        self.dim = 512
        self.depth = 1
        self.heads = 16
        self.mlp_dim = 1024
        self.w = 4
        self.b = 8
        self.s = True
        self.warm = 1
        self.lr = 1e-4
        self.uinch = 1
        self.imp_lr = 3e-4
        self.weights = 0
        self.base_weights = 0
        self.sim_weights = 0
        self.distributed = None
        self.dataset = 'isic'
        self.sam_ckpt = None
        self.thd = False
        self.chunk = 96
        self.num_sample = 4
        self.roi_size = 96
        self.evl_chunk = None
        self.data_path = ''

def parse_args():    
    opt = Arg()

    return opt
