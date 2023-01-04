import gradio as gr

from modules import script_callbacks

import os
import shutil
import pathlib

import argparse
import cv2
import torch
import numpy as np
from torch.cuda import amp
from PIL import Image

from modules.devices import get_optimal_device

def single(img, background = 'Transparent', fp32 = False, alt_mode = True, filename = 'tmp.png'):
    p = pathlib.Path(__file__).parts[-4:-2]
    path = os.path.abspath(f"{p[0]}/{p[1]}/{filename}")

    if not img:
        if os.path.exists(path):
            os.remove(path)
            print(f"{path} removed.")
        return

    # なぜかファイル経由じゃないとうまく処理できない
    img.save(path)

    animeseg(path, path, background, fp32, alt_mode)

    print(f"{path} saved.")

    img = Image.open(path)

    return img

def directory(input_dir, output_dir, background, fp32 = False, alt_mode = True):
    if not input_dir:
        raise ValueError("Please input Input_dir")
        return
    if not os.path.exists(input_dir):
        raise ValueError("Input_dir not found")
        return
    if not output_dir:
        raise ValueError("Please input Output_dir")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 全ファイルを処理
    for filename in os.listdir(input_dir):
        src_path = os.path.join(input_dir, filename)
        dst_path = os.path.join(output_dir, filename)
        animeseg(src_path, dst_path, background, fp32, alt_mode)

def animeseg(src_path, dst_path, background = 'Transparent', fp32 = False, alt_mode = True):
    p = pathlib.Path(__file__).parts[-4:-2]

    device = get_optimal_device()

    class Opt(object):
        def __init__(self):
            self.net = 'isnet_is'
            self.ckpt = f"{p[0]}/{p[1]}/anime-seg/isnetis.ckpt"
            self.device = str(device)
            self.fp32   = fp32
            self.img_size = 1024
    opt = Opt()

    import importlib
    inference = importlib.import_module(f"{p[0]}.{p[1]}.anime-segmentation.inference")
    get_mask = getattr(inference, 'get_mask')
    train = importlib.import_module(f"{p[0]}.{p[1]}.anime-segmentation.train")
    AnimeSegmentation = getattr(train, 'AnimeSegmentation')
    
    model = AnimeSegmentation.try_load(opt.net, opt.ckpt, opt.device)
    model.eval()
    model.to(device)

    img = cv2.cvtColor(cv2.imread(src_path, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    mask = get_mask(model, img, use_amp=not opt.fp32, s=opt.img_size)

    # 背景が黒でキャラが白
    if background == 'Mask':
        img = np.concatenate((img, mask * img, mask.repeat(3, 2) * 255), axis=1).astype(np.uint8)
        h, w, ch = img.shape
        img = img[0:, round(w*2/3):, :]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(dst_path, img)
    elif background == 'Transparent':
        if alt_mode:
            # anime-segのonly_mattedの実装
            img = np.concatenate((mask * img + 1 - mask, mask * 255), axis=2).astype(np.uint8)
        else:
            # anime-segのelse(jpeg出力)の実装
            img = np.concatenate((mask * img, mask * 255), axis=2).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)
        cv2.imwrite(dst_path, img)
    elif background == 'Black':
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)
        cv2.imwrite(dst_path, img)
    elif background == 'White':
        # 画像を読み込んでNumPy配列を作成
        img = np.concatenate((mask * img + 1 - mask, mask * 255), axis=2).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)

        if alt_mode:
            # なんでこれで直るのかわからんけどなぜかうまくいく
            R, G, B, A = cv2.split(img)
        else:
            B, G, R, A = cv2.split(img)
        alpha = A / 255

        R = (255 * (1 - alpha) + R * alpha).astype(np.uint8)
        G = (255 * (1 - alpha) + G * alpha).astype(np.uint8)
        B = (255 * (1 - alpha) + B * alpha).astype(np.uint8)

        image = cv2.merge((B, G, R))

        # アルファチャンネルのみの画像を作成して保存
        alpha_image = Image.fromarray(image)
        alpha_image.save(dst_path)
