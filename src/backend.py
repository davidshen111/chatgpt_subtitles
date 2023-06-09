import os
import json

from dotenv import load_dotenv, find_dotenv
from by_langchain import fetch_by_langchain_mapreduce, fetch_by_langchain_refine
from by_openai import fetch_by_openapi


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


def fetch_summaries(input_subtitles, operation_type='openai API'):    
    _ = load_dotenv(find_dotenv()) # read local .env file    
    split_args = {
        'trunk_size': int(os.environ['TRUNK_SIZE']),
        'overlap_size': int(os.environ['OVERLAP_SIZE']),
        'sentence_delimiter': os.environ['SENTENCE_DELIMITER']
    }
    input_subtitles_tmp = [item["content"] for item in input_subtitles["body"]]
    converted_subtitles = reconstruct_strings(input_subtitles_tmp, **split_args)

    if operation_type == 'openai API':      
        return fetch_by_openapi(converted_subtitles)
    if operation_type == 'langchain map-reduce': 
        return fetch_by_langchain_mapreduce(converted_subtitles)
    if operation_type == 'langchain refine': 
        return fetch_by_langchain_refine(converted_subtitles)    


if __name__ == "__main__":
    os.chdir('C:\\work\\chatgpt_subtitles\src')    
    input_subtitles = load_json_from_file('..\\test\\test1.json') 
    summaries = fetch_summaries(input_subtitles)
    print(summaries)



