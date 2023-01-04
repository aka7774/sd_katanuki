import gradio as gr

from katanuki import animeseg, layer

from modules import script_callbacks
import modules.shared as shared

def on_ui_tabs():
    with gr.Blocks() as katanuki_interface:
        with gr.Row(equal_height=True):
            background = gr.Radio(choices=["None", "Transparent", "White", "Mask"], value="Transparent", label="Katanuki")
            fp32 = gr.Checkbox(label="Use FP32(for 16X0)")
            alt_mode = gr.Checkbox(value=True, label="Alt mode")
        with gr.Tabs(elem_id="katanuki"):
            with gr.TabItem('Single Image'):
                with gr.Row(equal_height=True):
                    with gr.Column(variant='panel'):
                        src_image = gr.Image(label="Source", source="upload", interactive=True, type="pil")
                    with gr.Column(variant='panel'):
                        dst_image = gr.Image(label="Result", interactive=False, type="pil")
            with gr.TabItem('Directory'):
                input_dir = gr.Textbox(label="Input directory")
                output_dir = gr.Textbox(label="Output directory")
                dir_run = gr.Button(elem_id="dir_run", label="Generate", variant='primary')
            with gr.TabItem('Layer'):
                layer_html = gr.HTML('''
                <ol>
                <li>1. Upload background image, Send
                <li>2. Push Upload image x button, Upload characher image, Send
                <li>3. Change Position and Scale slider, Merge(redoable)
                <li>4. goto 2
                <li>5. Cleanup: Push "Delete All Temporary Images" button
                </ol>
                ''')
                layer_reset = gr.Button("Delete All Temporary Images")
                layer_src_image = gr.Image(label="Upload", source="upload", interactive=True, type="pil")
                layer_send = gr.Button("Send")
                layer_position_x = gr.Slider(
                minimum=-2048, #-layer.get_x(),
                maximum=2048, #layer.get_x(),
                value=0,
                step=1,
                label='X Position'
                )
                layer_position_y = gr.Slider(
                minimum=-2048, #-layer.get_y(),
                maximum=2048, #layer.get_y(),
                value=0,
                step=1,
                label='Y Position'
                )
                layer_scale = gr.Slider(
                minimum=0.5,
                maximum=2,
                value=1,
                step=0.05,
                label='Scale'
                )
                layer_mirror = gr.Checkbox(label="Mirror")
                layer_merge = gr.Button("Merge")
                layer_dst_image = gr.Image(label="Result", source="upload", interactive=False, type="pil")

        src_image.change(
            fn=animeseg.single,
            inputs=[src_image, background, fp32, alt_mode],
            outputs=[dst_image],
        )

        dir_run.click(
            fn=animeseg.directory,
            inputs=[input_dir, output_dir, background, fp32, alt_mode]
        )

        layer_reset.click(
            fn=layer.reset,
            inputs=[],
            outputs=[],
        )

        layer_send.click(
            fn=layer.upload,
            inputs=[layer_src_image, background, fp32, alt_mode],
            outputs=[layer_dst_image],
        )

        layer_merge.click(
            fn=layer.slide,
            inputs=[layer_position_x, layer_position_y, layer_scale, layer_mirror],
            outputs=[layer_dst_image],
        )

    return (katanuki_interface, "Katanuki", "katanuki_interface"),


script_callbacks.on_ui_tabs(on_ui_tabs)
