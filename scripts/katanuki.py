import os

import gradio as gr

from katanuki import animeseg

from modules import script_callbacks
import modules.shared as shared
import modules.scripts as scripts
from modules import images
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state

class Script(scripts.Script):
    def title(self):
        return "Katanuki"

    def ui(self, is_img2img):
        with gr.Row():
            background = gr.CheckboxGroup(choices=["Transparent", "White", "Mask"], label="Background")
        with gr.Row():
            fp32 = gr.Checkbox(label="Use FP32(for 16X0)")
            alt_mode = gr.Checkbox(value=True, label="Alt mode")

        return [background, fp32, alt_mode]

    def show(self, is_img2img):
        return True

    def run(self, p, background, fp32, alt_mode):
        proc = process_images(p) 
        for i in range(len(proc.images)):
            for bg in background:
                img = animeseg.single(proc.images[i], bg, fp32, alt_mode)
                images.save_image(img, p.outpath_samples, bg)
                proc.images.append(img)

        # tmpの片づけ
        animeseg.single(None)

        return proc
