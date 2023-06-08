import gradio as gr
import json
from backend import fetch_summaries, load_json_from_file
import os

def run_ui():
    gr.Interface(
        run_ui_logic,
        [gr.components.File(label='Upload your file'),  gr.Radio(["openai API", "langchain map-reduce", "langchain refine"], label="Select summarizing method"),],
        outputs =  ['text'],
        title='Subtitles Summarizer',
        allow_flagging="never"
    ).launch() 

def run_ui_logic(json_file, operation_type):
    with open(json_file.name, 'r', encoding="utf8") as file:
        json_str = file.read()
    json_data = json.loads(json_str)
    summaries = fetch_summaries(json_data)
    return summaries

if __name__ == '__main__':
    os.chdir('C:\\work\\chatgpt_subtitles\src')
    run_ui()

    


