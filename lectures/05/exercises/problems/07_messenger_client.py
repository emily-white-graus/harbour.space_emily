"""Problem 07 (part B): messenger sender client.

Task:
1. Split into pairs
2. Write an infinite loop reading message text from terminal
3. Send each message to partner API endpoint /messages
4. Show send status in terminal


Partner setup:
- Partner gives you ngrok public URL
- You set TARGET_BASE_URL to that URL
"""

import requests

TARGET_BASE_URL = "https://replace-with-partner-ngrok-url"
SENDER_NAME = "replace-with-your-name"


def main() -> None:
    # TODO: implement input loop and POST sending
    while True:
        text = input("Message (or 'quit'): ").strip()
        if text.lower() == "quit":
            break
        if not text:
            continue

        response = requests.post(
            f"{TARGET_BASE_URL}/messages",
            json={"sender": SENDER_NAME, "text": text},
            timeout=10,
        )

        print("Status:", response.status_code)
        try:
            print("Response:", response.json())
        except ValueError:
            print("Response:", response.text)


if __name__ == "__main__":
    main()
