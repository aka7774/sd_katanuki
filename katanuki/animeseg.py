import gradio as gr

from modules import script_callbacks

import os

import argparse
import cv2
import torch
import numpy as np
import glob
from torch.cuda import amp
from tqdm import tqdm
from PIL import Image

def run(img):
    class Opt(object):
        def __init__(self):
            self.net = 'isnet_is'
            self.ckpt = 'extensions/sd_katanuki/anime-seg/isnetis.ckpt'
            self.device = 'cuda:0'
            self.fp32   = False
            self.img_size = 1024
    opt = Opt()

    import importlib
    inference = importlib.import_module("extensions.sd_katanuki.anime-segmentation.inference")
    get_mask = getattr(inference, 'get_mask')
    train = importlib.import_module("extensions.sd_katanuki.anime-segmentation.train")
    AnimeSegmentation = getattr(train, 'AnimeSegmentation')
    
    device = torch.device(opt.device)

    model = AnimeSegmentation.try_load(opt.net, opt.ckpt, opt.device)
    model.eval()
    model.to(device)

    # なぜかファイル経由じゃないとうまく処理できない
    path = 'extensions/sd_katanuki/tmp.png'
    try:
        img.save(path)
    except:
        print()

    img = cv2.cvtColor(cv2.imread(path, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    mask = get_mask(model, img, use_amp=not opt.fp32, s=opt.img_size)
    img = np.concatenate((mask * img + 1 - mask, mask * 255), axis=2).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)
    cv2.imwrite(path, img)
    img = Image.open(path)

    try:
        os.remove(path)
    except:
        print()

    return img
