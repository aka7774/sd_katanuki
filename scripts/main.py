import gradio as gr

from katanuki import animeseg

from modules import script_callbacks
import modules.shared as shared

def on_ui_tabs():
    with gr.Blocks() as katanuki_interface:
        with gr.Row(equal_height=True):
            background = gr.Radio(choices=["Transparent", "White"], value="Transparent", label="Background")
            fp32 = gr.Checkbox(label="Use FP32(for 16X0, CPU...)")
        with gr.Tabs(elem_id="katanuki"):
            with gr.TabItem('Single Image'):

                with gr.Row(equal_height=True):
                    with gr.Column(variant='panel'):
                        src_image = gr.Image(label="Source", source="upload", interactive=True, type="pil")
                    with gr.Column(variant='panel'):
                        dst_image = gr.Image(label="Result", interactive=False, type="pil")
            with gr.TabItem('Directory'):
                input_dir = gr.Textbox(label="Input directory", **shared.hide_dirs, placeholder="A directory on the same machine where the server is running.")
                output_dir = gr.Textbox(label="Output directory", **shared.hide_dirs, placeholder="Leave blank to save images to the Input directory.")
                dir_run = gr.Button(elem_id="dir_run", label="Generate", variant='primary')

        src_image.change(
            fn=animeseg.single,
            inputs=[src_image, background, fp32],
            outputs=[dst_image],
        )

        dir_run.click(
            fn=animeseg.directory,
            inputs=[input_dir, output_dir, background, fp32]
        )

    return (katanuki_interface, "Katanuki", "katanuki_interface"),


script_callbacks.on_ui_tabs(on_ui_tabs)
