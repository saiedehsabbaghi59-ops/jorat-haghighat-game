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
                    "text": "🎮 به بازی جرئت یا حقیقت خوش آمدی!\n\nبرای شروع بازی روی دکمه زیر بزن.",
                    "reply_markup": {
                        "inline_keyboard": [[
                            {
                                "text": "🎮 شروع بازی",
                                "web_app": {
                                    "url": "https://saiedehsabbaghi59-ops.github.io/jorat-haghighat-game/"
                                }
                            }
                        ]]
                    }
                },
                timeout=10
            )
    return "OK"

    return "OK"
    
WEBHOOK_URL = "https://jorat-haghighat-game.onrender.com/webhook"

requests.post(
    f"{API}/setWebhook",
    json={"url": WEBHOOK_URL},
    timeout=10
)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
