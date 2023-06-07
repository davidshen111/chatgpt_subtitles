import json
from flask import Flask, request, jsonify

from backend import fetch_summaries

app = Flask(__name__)

@app.route('/summaries/bilibili', methods=['POST'])
def process_summary():
    data = json.loads(request.data) 
    summaries = fetch_summaries(data)
    result = {'data': summaries}
    return jsonify(result)
   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)