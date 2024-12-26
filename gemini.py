import json
import requests

from Jarvis_main import GEMINI_API_URL


def get_gemini_response(question):
    headers = {
        "Authorization": f"Bearer {'AIzaSyAsJd2zqDpRYwKQAAHAE2OZIIDqTRK3reA'}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gemini-chat-model",  # Replace with the appropriate model
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for error HTTP status codes
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching response: {e}")
        return "Unable to retrieve response due to an error."
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}")
        return "Unable to retrieve response due to an error."