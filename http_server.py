import json
from flask import Flask, request, jsonify

from backend import fetch_summaries

app = Flask(__name__)

@app.route('/summaries/bilibili', methods=['POST'])
def process_summary():
    #file_key = list(request.files.keys())[0]  
    #file = request.files[file_key]
    #data = file.read()  
    #json_data = data.decode('utf-8')  
    #json_dict = json.loads(json_data)  
    data = json.loads(request.data) 
    summaries = fetch_summaries(data)
    result = {'data': summaries}
    return jsonify(result)
   

if __name__ == '__main__':
    import os
    os.chdir('C:\\work\\chatgpt_subtitles')    
    app.run(host='0.0.0.0', port=8000)