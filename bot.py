import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("BALE_TOKEN")
API = f"https://tapi.bale.ai/bot{TOKEN}"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    message = data.get("message", {})
    chat = message.get("chat", {})
    text = message.get("text", "")

    if text == "/start":
        chat_id = chat.get("id")

        if chat_id:
            requests.post(
                f"{API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "🎮 به بازی جرئت یا حقیقت خوش آمدی!\n\nبرای شروع بازی روی دکمه بازی بزن."
                },
                timeout=10
            )

    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
