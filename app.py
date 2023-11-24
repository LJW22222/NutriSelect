import openai
import os
import time
from flask import Flask, jsonify, render_template, request
from decouple import config

app = Flask(__name__)

openai.api_key = config('OPENAI_API_KEY')

def get_ai_response(question):
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question},
    ]
    start_time = time.time()  # 시작 시간 측정
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    end_time = time.time()  # 종료 시간 측정
    elapsed_time = end_time - start_time  # 경과 시간 계산
    
    return response['choices'][0]['message']['content'], elapsed_time


def chatgpt():
    while True:
        question = input("나 : ")
        
        if question.lower() == 'exit':
            break
        
        assistant_content, elapsed_time = get_ai_response(question)

        print(f"AI: {assistant_content}")
        print(f"경과 시간: {elapsed_time:.2f} s")

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/send-message", methods=['POST'])
def send_message():
    user_message = request.json['message']
    assistant_content, elapsed_time = get_ai_response(user_message)
    return jsonify({'message': assistant_content})
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3535, debug=True)