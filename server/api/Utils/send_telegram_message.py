import requests
from django.conf import settings


def send_telegram_message(TG_ID: str, text: str):
    url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)
