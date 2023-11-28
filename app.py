import openai
import os
import time
from flask import Flask, jsonify, render_template, request
from decouple import config

app = Flask(__name__)

openai.api_key = config('OPENAI_API_KEY')

# Initialize conversation outside the function to maintain state
conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
]

def get_ai_response(question):
    global conversation  # Reference the global variable
    conversation.append({"role": "user", "content": question})
    
    start_time = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Update conversation with AI response
    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    
    return response['choices'][0]['message']['content'], elapsed_time


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
