import gradio as gr

from modules import script_callbacks

import os
import shutil

import argparse
import cv2
import torch
import numpy as np
import glob
from torch.cuda import amp
from tqdm import tqdm
from PIL import Image

def single(img, background = 'Transparent', fp32 = False):
    path = 'extensions/sd_katanuki/tmp.png'

    if not img:
        if os.path.exists(path):
            os.remove(path)
            print(f"{path} removed.")
        return

    # なぜかファイル経由じゃないとうまく処理できない
    img.save(path)

    animeseg(path, background, fp32)

    print(f"{path} saved.")

    img = Image.open(path)

    return img

def directory(input_dir, output_dir, background, fp32 = False):
    if not input_dir:
        print("input_dir needed.")
        return

    # output_dirに加工前のファイルをまとめる
    if not output_dir:
        output_dir = input_dir
    else:
        shutil.copytree(input_dir, output_dir, dirs_exist_ok=True)

    # output_dirの全ファイルを処理
    for i, path in enumerate(tqdm(sorted(glob.glob(f"{output_dir}/*.*")))):
        animeseg(path, background, fp32)

def animeseg(path, background = 'Transparent', fp32 = False):
    class Opt(object):
        def __init__(self):
            self.net = 'isnet_is'
            self.ckpt = 'extensions/sd_katanuki/anime-seg/isnetis.ckpt'
            self.device = 'cuda:0'
            self.fp32   = fp32
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

    img = cv2.cvtColor(cv2.imread(path, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    mask = get_mask(model, img, use_amp=not opt.fp32, s=opt.img_size)
    img = np.concatenate((mask * img + 1 - mask, mask * 255), axis=2).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)

    if background != 'White':
        cv2.imwrite(path, img)

    if background == 'White':
        # 画像を読み込んでNumPy配列を作成
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)

        B, G, R, A = cv2.split(img)
        alpha = A / 255

        R = (255 * (1 - alpha) + R * alpha).astype(np.uint8)
        G = (255 * (1 - alpha) + G * alpha).astype(np.uint8)
        B = (255 * (1 - alpha) + B * alpha).astype(np.uint8)

        image = cv2.merge((B, G, R))

        # アルファチャンネルのみの画像を作成して保存
        alpha_image = Image.fromarray(image)
        alpha_image.save(path)
