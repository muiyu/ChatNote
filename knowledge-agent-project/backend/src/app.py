from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.knowledge_agent import process_question_only, process_markdown_with_llm  # 假设这是处理仅问题的函数
import os

app = Flask(__name__)
CORS(app)  # 启用 CORS 支持

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        if file.filename.endswith('.md'):
            markdown_content = file.read().decode('utf-8') 
            question = request.form.get('question', '默认问题')  
            print("Received file:", file.filename)  
            print("Question:", question) 

            llm_response = process_markdown_with_llm(markdown_content, question)
            print("调试app.py", llm_response)
            return jsonify({"response": llm_response}), 200
        else:
            return jsonify({"error": "File must be a Markdown (.md) file"}), 400
    except Exception as e:
        print("Error:", str(e)) 
        return jsonify({"error": str(e)}), 500  

@app.route('/question', methods=['POST'])
def handle_question():
    try:
        data = request.get_json()
        question = data.get('question', '默认问题')  
        print("Received question:", question) 

        response = process_question_only(question)
        print("调试app.py", response)
        return jsonify({"response": response}), 200
    except Exception as e:
        print("Error:", str(e))  
        return jsonify({"error": str(e)}), 500  

if __name__ == '__main__':
    app.run(debug=True)