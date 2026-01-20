"""Entry point for the AI Ask About Me Gradio application."""

from dotenv import load_dotenv
import gradio as gr
from ai_ask_about_me import MeAgent

# Load environment variables
load_dotenv(override=True)

if __name__ == "__main__":
    me = MeAgent()
    gr.ChatInterface(me.chat).launch()
