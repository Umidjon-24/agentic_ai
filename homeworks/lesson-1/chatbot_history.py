import time
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv('.env')

client = genai.Client()
HISTORY_FILE = "history.json"

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

history = load_history()

def gemini_contents(history):
    contents = []
    for msg in history:
        role = "model" if msg["role"] in ("model") else "user"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])]
            )
        )
    return contents

while True:
    user_input = input("User: ")

    history.append({"role": "user", "content": user_input})

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=gemini_contents(history),
    )

    ai_reply = response.text
    print("AI:", ai_reply)

    history.append({"role": "model", "content": ai_reply})
    save_history(history)

    time.sleep(0.5)
