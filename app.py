from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Store chat history (list of dicts with role and content)
chat_history = []

@app.route('/', methods=['GET', 'POST'])
def chat():
    global chat_history
    if request.method == 'POST':
        user_input = request.form['message']
        # Add user's message to history
        chat_history.append({"role": "user", "content": user_input})

        # Prepare API request with full chat history
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "I’m a pregnancy assistant built by Victor to help you, my dear sister!"}
            ] + chat_history,  # Include full history for context
            "max_tokens": 500
        }
        api_response = requests.post(GROQ_URL, json=payload, headers=headers)
        if api_response.status_code == 200:
            bot_response = api_response.json()["choices"][0]["message"]["content"]
            # Add bot's response to history
            chat_history.append({"role": "assistant", "content": bot_response})
        else:
            chat_history.append({"role": "assistant", "content": "Oops! Something went wrong—Victor’s fixing it!"})

    return render_template('index.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)