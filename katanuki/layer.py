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

from . import animeseg

def get_x():
    p = pathlib.Path(__file__).parts[-4:-2]
    merged_path = os.path.abspath(f"{p[0]}/{p[1]}/merged.png")
    if not os.path.exists(merged_path):
        return 0
    base = Image.open(merged_path)
    return base.size[0]

def get_y():
    p = pathlib.Path(__file__).parts[-4:-2]
    merged_path = os.path.abspath(f"{p[0]}/{p[1]}/merged.png")
    if not os.path.exists(merged_path):
        return 0
    base = Image.open(merged_path)
    return base.size[1]

def reset():
    animeseg.single(None, '', False, False, 'merged.png')
    animeseg.single(None, '', False, False, 'layer.png')
    animeseg.single(None, '', False, False, 'tmp.png')

def merge(merged_path, layer_path, left = 0, top = 0, scale = 1):
    base = Image.open(merged_path)
    layer = Image.open(layer_path)

    if scale != 1:
        layer = layer.resize((int(layer.size[0] * scale), int(layer.size[1] * scale)))

    base.paste(layer, (left, top), layer)
    return base

def slide(left, top, scale):
    p = pathlib.Path(__file__).parts[-4:-2]
    merged_path = os.path.abspath(f"{p[0]}/{p[1]}/merged.png")
    layer_path = os.path.abspath(f"{p[0]}/{p[1]}/layer.png")
    tmp_path = os.path.abspath(f"{p[0]}/{p[1]}/tmp.png")

    if not os.path.exists(merged_path):
        raise ValueError(f"Not found {merged_path}")
    if not os.path.exists(layer_path):
        raise ValueError(f"Not found {layer_path}")

    img = merge(merged_path, layer_path, left, top, scale)
    img.save(tmp_path)

    return img

def upload(img, background = 'Transparent', fp32 = False, alt_mode = True):
    p = pathlib.Path(__file__).parts[-4:-2]
    merged_path = os.path.abspath(f"{p[0]}/{p[1]}/merged.png")
    layer_path = os.path.abspath(f"{p[0]}/{p[1]}/layer.png")
    tmp_path = os.path.abspath(f"{p[0]}/{p[1]}/tmp.png")

    # xボタンが押された
    if not img:
        if os.path.exists(merged_path):
            return Image.open(merged_path)
        else:
            return

    # 1枚目の画像が来た
    if not os.path.exists(merged_path):
        img.save(merged_path)
        img.save(tmp_path)
        return img

    # 3枚目の画像が来たら2枚目の画像の位置を確定
    if os.path.exists(layer_path):
        shutil.copyfile(tmp_path, merged_path)

    # 2枚目以降の画像が来た
    img = animeseg.single(img, background, fp32, alt_mode, 'layer.png')
    img = merge(merged_path, layer_path)
    img.save(tmp_path)

    return img
