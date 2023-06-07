import os
import openai
import sys
import utils
import json

from dotenv import load_dotenv, find_dotenv


def load_json_from_file(file_name):
    try:
        with open(file_name, encoding="utf8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error occurred while loading file '{file_name}': {str(e)}")
    return []


def reconstruct_strings(strings, trunk_size, overlap_size, sentence_delimiter):
    result = []
    current_part = ""
    current_length = 0
    total_length = sum(len(string) for string in strings)

    if (total_length <= trunk_size):
        result.append(sentence_delimiter.join(strings)) 
        return result    

    start_index = -1
    for i in range(len(strings)):
        string = strings[i]
        if start_index == -1:
            if current_length + len(string) + 1 > trunk_size - overlap_size:
                start_index = i
        if current_length + len(string) + 1 >= trunk_size:
            result.append(current_part)
            break
        current_part += sentence_delimiter + string
        current_length = len(current_part) - 1
    
    if start_index != -1:
        remaining_strings = strings[start_index + 1:]
        if remaining_strings:
            result.extend(reconstruct_strings(remaining_strings, trunk_size, overlap_size, sentence_delimiter))

    return result


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=1000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    print(response.usage)
    return response.choices[0].message["content"]


def message_template_1 (user_message_1):
    delimiter = "####"
    system_message = f"""
    Your task is to generate an overall summary using the user's input. \
    The user's input will be delimited by {delimiter} characters. \
    The output should be a text in UTF-8 format, written in Chinese. 
    """   
    messages =  [ 
        {'role':'system', 
         'content': system_message}, 
        {'role':'user',
         'content': f"{delimiter}{user_message_1}{delimiter}"}  
    ] 
    return messages


def message_template_2 (user_message_1, user_message_2):
    delimiter = "####"
    system_message = f"""
    Your task is to generate an overall summary using the previous summary plus user's new input. \
    This is an accumulative task. \
    The previous summary is enclosed within {delimiter} as shown below: {delimiter}{user_message_1}{delimiter} \

    Summarize the user's new input and incorporate it into the existing summary as the output. \
    Update the output to ensure its coherence. \
    The user's new input will be enclosed by {delimiter} characters. \
    The output should be a UTF-8 encoded text written in Chinese. \
    """   
    messages =  [ 
        {'role':'system', 
         'content': system_message}, 
        {'role':'user',
         'content': f"{delimiter}{user_message_2}{delimiter}"}  
    ] 
    return messages

def fetch_summaries(input_subtitles):
    _ = load_dotenv(find_dotenv()) # read local .env file
    openai.api_key  = os.environ['OPENAI_API_KEY']
    split_args = {
        'trunk_size': int(os.environ['TRUNK_SIZE']),
        'overlap_size': int(os.environ['OVERLAP_SIZE']),
        'sentence_delimiter': os.environ['SENTENCE_DELIMITER']
    }
    input_subtitles_tmp = [item["content"] for item in input_subtitles["body"]]
    converted_subtitles = reconstruct_strings(input_subtitles_tmp, **split_args)
    for index, subtitle in enumerate(converted_subtitles):
        if (index ==0):
            messages = message_template_1(subtitle)
        else:
            messages = message_template_2(summaries, subtitle)
        summaries = get_completion_from_messages(messages)
    return summaries         


if __name__ == "__main__":
    # os.chdir('C:\\work\\chatgpt_subtitles\src')    
    input_subtitles = load_json_from_file('.\\test\\test1.json') 
    summaries = fetch_summaries(input_subtitles)
    print(summaries)



