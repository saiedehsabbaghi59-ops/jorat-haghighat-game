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


def send_message(chat_id, text, keyboard=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }

    if keyboard:
        data["reply_markup"] = {
            "inline_keyboard": keyboard
        }

    requests.post(
        f"{API}/sendMessage",
        json=data,
        timeout=10
    )


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}

    message = data.get("message", {})
    callback = data.get("callback_query", {})

    chat = message.get("chat", {})
    text = message.get("text", "")
    chat_id = chat.get("id")

    # /start
    if text == "/start" and chat_id:

        if not is_member(chat_id):
            send_message(
                chat_id,
                "🔒 برای استفاده از بازی، ابتدا عضو کانال ما شو 👇",
                [
                    [
                        {
                            "text": "📢 عضویت در کانال",
                            "url": "https://ble.ir/chocolate_land_channle"
                        }
                    ],
                    [
                        {
                            "text": "✅ بررسی عضویت",
                            "callback_data": "check_member"
                        }
                    ]
                ]
            )
        else:
            send_message(
                chat_id,
                "🎮 به بازی جرئت یا حقیقت خوش آمدی!\n\nبرای شروع بازی روی دکمه زیر بزن.",
                [
                    [
                        {
                            "text": "🎮 شروع بازی",
                            "web_app": {
                                "url": GAME_URL
                            }
                        }
                    ]
                ]
            )

    # بررسی عضویت
    if callback:
        callback_id = callback.get("id")
        callback_data = callback.get("data")
        callback_message = callback.get("message", {})
        callback_chat = callback_message.get("chat", {})
        callback_chat_id = callback_chat.get("id")

        if callback_data == "check_member" and callback_chat_id:

            if is_member(callback_chat_id):

                requests.post(
                    f"{API}/answerCallbackQuery",
                    json={
                        "callback_query_id": callback_id,
                        "text": "✅ عضویت شما تأیید شد!"
                    },
                    timeout=10
                )

                send_message(
                    callback_chat_id,
                    "🎉 عضویتت تأیید شد!\n\nحالا می‌تونی بازی رو شروع کنی.",
                    [
                        [
                            {
                                "text": "🎮 شروع بازی",
                                "web_app": {
                                    "url": GAME_URL
                                }
                            }
                        ]
                    ]
                )

            else:

                requests.post(
                    f"{API}/answerCallbackQuery",
                    json={
                        "callback_query_id": callback_id,
                        "text": "❌ هنوز عضو کانال نیستی."
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
