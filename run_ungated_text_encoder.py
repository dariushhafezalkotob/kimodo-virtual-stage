#!/usr/bin/env python3
"""
Ungated Text Encoder Server for Kimodo AI Virtual Stage.
Directly instantiates LLM2VecEncoder using the ungated NousResearch/Meta-Llama-3-8B-Instruct repository.
Uses bfloat16 precision to fit comfortably in memory.
"""
import os
import sys
import argparse
import numpy as np
import gradio as gr
import torch

from kimodo.model.llm2vec.llm2vec_wrapper import LLM2VecEncoder
from kimodo.scripts.gradio_theme import get_gradio_theme

DEFAULT_TEXT = "A person walks and waves."
DEFAULT_SERVER_NAME = "0.0.0.0"
DEFAULT_SERVER_PORT = 9550
DEFAULT_TMP_FOLDER = "/tmp/text_encoder/"


class DemoWrapper:
    def __init__(self, text_encoder, tmp_folder):
        self.text_encoder = text_encoder
        self.tmp_folder = tmp_folder

    def __call__(self, text, filename, progress=gr.Progress()):
        tensor, length = self.text_encoder(text)
        embedding = tensor[:length].cpu().numpy()
        path = os.path.join(self.tmp_folder, filename)
        np.save(path, embedding)

        output_title = gr.Markdown(visible=True)
        output_text = gr.Markdown(visible=True, value=f"Text: {text}")
        download = gr.DownloadButton(visible=True, value=path)
        return download, output_title, output_text


def main():
    server_name = os.getenv("GRADIO_SERVER_NAME", DEFAULT_SERVER_NAME)
    server_port = int(os.getenv("GRADIO_SERVER_PORT", DEFAULT_SERVER_PORT))
    tmp_folder = os.getenv("TEXT_ENCODER_TMP_FOLDER", DEFAULT_TMP_FOLDER)
    os.makedirs(tmp_folder, exist_ok=True)

    device = os.getenv("TEXT_ENCODER_DEVICE", "cpu")
    dtype = "bfloat16"

    print("=================================================================", flush=True)
    print(f"Loading Ungated LLM2Vec Text Encoder on {device} (dtype={dtype})...", flush=True)
    print("Base Model: NousResearch/Meta-Llama-3-8B-Instruct (Ungated)", flush=True)
    print("=================================================================", flush=True)

    text_encoder = LLM2VecEncoder(
        base_model_name_or_path="NousResearch/Meta-Llama-3-8B-Instruct",
        peft_model_name_or_path="McGill-NLP/LLM2Vec-Meta-Llama-3-8B-Instruct-mntp-supervised",
        dtype=dtype,
        llm_dim=4096,
        device=device,
    )

    print("LLM2Vec Model loaded successfully into memory!", flush=True)
    print(f"Starting Gradio service on http://{server_name}:{server_port} ...", flush=True)

    theme, css = get_gradio_theme()
    demo_wrapper_fn = DemoWrapper(text_encoder, tmp_folder)

    with gr.Blocks(theme=theme, css=css) as demo:
        gr.Markdown("# Kimodo Text Encoder (Ungated)")
        text_input = gr.Textbox(value=DEFAULT_TEXT, label="Text")
        filename_input = gr.Textbox(value="embedding.npy", label="Filename")
        btn = gr.Button("Encode")
        download_btn = gr.DownloadButton(visible=False)
        out_title = gr.Markdown(visible=False)
        out_text = gr.Markdown(visible=False)
        btn.click(
            demo_wrapper_fn,
            inputs=[text_input, filename_input],
            outputs=[download_btn, out_title, out_text],
        )

    demo.queue()
    demo.launch(server_name=server_name, server_port=server_port, share=False)


if __name__ == "__main__":
    main()
