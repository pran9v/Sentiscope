from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import json
import re

app = Flask(__name__)
CORS(app)

@app.route('/process_emotion', methods=['POST'])
def process_emotion():
    data = request.json
    text = data.get('text')
   
    if not text:
        return jsonify({'error(app.py)': 'Please provide a text parameter'}), 400

    try:
        # Run the Python script to process emotions
        process = subprocess.Popen(['python', 'script.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        input_data = json.dumps({'action': 'analyzeText', 'text': text})
        
        output, error = process.communicate(input=input_data)
        match = re.search(r'\b(\w+)$', output)
        emotion = match.group(1)

        # return the plain string output from script.py
        return emotion

    except Exception as e:
        print("Error in Flask app(app.py):", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
