import requests
import json
from config import WHATSAPP_TOKEN

WHATSAPP_URL = "https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages"

def send_whatsapp_message(to, message):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(WHATSAPP_URL, headers=headers, json=payload)
    return response.json()
