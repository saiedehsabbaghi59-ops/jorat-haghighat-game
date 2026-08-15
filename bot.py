import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("BALE_TOKEN")
API = f"https://tapi.bale.ai/bot{TOKEN}"

CHANNEL = "@chocolate_land_channle"
GAME_URL = "https://saiedehsabbaghi59-ops.github.io/jorat-haghighat-game/"


@app.route("/", methods=["GET"])
def home():
    return "Bot is running"


def is_member(chat_id):
    try:
        response = requests.post(
            f"{API}/getChatMember",
            json={
                "chat_id": CHANNEL,
                "user_id": chat_id
            },
            timeout=10
        )

        result = response.json()

        if not result.get("ok"):
            return False

        member = result.get("result", {})
        status = member.get("status")

        return status in ["creator", "administrator", "member"]

    except Exception:
        return False


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    message = data.get("message", {})
    chat = message.get("chat", {})
    text = message.get("text", "")
    chat_id = chat.get("id")

    if text == "/start" and chat_id:

        if not is_member(chat_id):
            requests.post(
                f"{API}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "🔒 برای استفاده از بازی، ابتدا باید عضو کانال ما شوی:\n\n@chocolate_land_channle\n\nبعد از عضویت دوباره /start را بزن.",
                },
                timeout=10
            )
            return "OK"

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
                                "url": GAME_URL
                            }
                        }
                    ]]
                }
            },
            timeout=10
        )

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
