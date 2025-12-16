import time
from dotenv import load_dotenv

load_dotenv('.env')

from google import genai

client = genai.Client()
while(True):
    print("User: ")
    response = client.models.generate_content(
        model="gemma-3-12b",
        contents=input(),
    )

    print("AI: ", response.text)
    time.sleep(0.5)
