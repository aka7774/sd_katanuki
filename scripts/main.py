import gradio as gr

from katanuki import animeseg

from modules import script_callbacks

def on_ui_tabs():
    with gr.Blocks() as katanuki_interface:
        with gr.Row(equal_height=True):
            with gr.Column(variant='panel'):
                src_image = gr.Image(label="Source", source="upload", interactive=True, type="pil")
            with gr.Column(variant='panel'):
                dst_image = gr.Image(label="Result", interactive=False, type="pil")

            src_image.change(
                fn=animeseg.run,
                inputs=[src_image],
                outputs=[dst_image],
            )

    return (katanuki_interface, "Katanuki", "katanuki_interface"),


script_callbacks.on_ui_tabs(on_ui_tabs)
