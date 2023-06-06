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
            content_list = [item["content"] for item in data["body"]]
        return content_list
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
    You are a proficient English teacher who excels in English writing and English-Chinese translation. \ 
    Your task is to generate a overall summary and the parapragh's summaries based on user's input: \
    The user's input will be delimited with {delimiter} characters. \
    Follow below steps to generate the output: \
    Step 1 - Translate the user's input from Chinese to English. \
    Step 2 - Segment the user's input into several segmentations and summarize them repsectively. \
             Delete the similar summaries if having. \
             Use at most 80 words for each summary. \
    Step 3 - Generate a overall summary.\
             Use at most 80 words. \
    Step 4 - Tanslate the segmentations' summaries and the overall summary into Chinese. \        
    
    The output must be a JSON string encoded in UTF-8, written in Chinese. and following the format: \
    {{
        "overall": "",
        "segmentations": [
            "",
            "",
            ...
        ]
    }} 
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
    delimiter1 = "#*#*"
    system_message = f"""
    You are a proficient English teacher who excels in English writing and English-Chinese translation. \ 
    Your task is to create a overall summary and the parapragh's summaries based on user's input: \
    The user's input will be delimited with {delimiter} characters. \
    This task is cumulative, and you already have the summary of the previous part of user's input. \
    The summary includes one overall summray and several segmentations' summaries. \
    It's delimited by {delimiter1} and follows the format: \
    {{
        "overall": "",
        "segmentations": [
            "",
            "",
            ...
        ]
    }} \
    Previous summary: {delimiter1}{user_message_1}{delimiter1} \

    Follow below steps to generate the output: \
    Step 1 - Translate previous summary from Chinese to English. \
    Step 2 - Translate user's input from Chinese to English. \
    Step 3 - Segment the user's input, summarize the segmentations and append them into the existing segmentations' summaries. \
             Delete the similar segmentations' summaries. \
             Use at most 80 words for each summary. \
    Step 4 - Update the existing overall summary by accumulating the new user's input. \
             Do not simply overwrite the previous overall summary. \
             Use at most 80 words. \
    Step 5 - Tanslate the result from step 3 and step 4 into Chinese. \           
         
    This output must be a JSON string encoded in UTF-8, written in Chinese, and following the format: \
    {{
        "overall": "",
        "segmentations": [
            "",
            "",
            ...
        ]
    }} 
    """   
    messages =  [ 
        {'role':'system', 
         'content': system_message}, 
        {'role':'user',
         'content': f"{delimiter}{user_message_2}{delimiter}"}  
    ] 
    return messages

# os.chdir('C:\\work\\chatgpt_subtitles')
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.environ['OPENAI_API_KEY']
split_args = {
    'trunk_size': int(os.environ['TRUNK_SIZE']),
    'overlap_size': int(os.environ['OVERLAP_SIZE']),
    'sentence_delimiter': os.environ['SENTENCE_DELIMITER']
}


input_subtitles = load_json_from_file('test1.json') 
converted_subtitles = reconstruct_strings(input_subtitles, **split_args)

for index, subtitle in enumerate(converted_subtitles):
    if (index ==0):
        messages = message_template_1(subtitle)
    else:
        messages = message_template_2(summaries, subtitle)
    summaries = get_completion_from_messages(messages) 
    print(summaries)

