import os
import requests
import google.generativeai as genai
from flask import Flask, request

# Configurar Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configurar Flask
app = Flask(__name__)

# Token de WhatsApp API
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_URL = "https://graph.facebook.com/v18.0/me/messages"

# Función para enviar mensajes de WhatsApp
def send_whatsapp_message(phone, message):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    response = requests.post(WHATSAPP_URL, headers=headers, json=data)
    return response.json()

# Ruta Webhook para recibir mensajes de WhatsApp
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data.get("entry"):
        for entry in data["entry"]:
            for message in entry["changes"]:
                phone = message["value"]["messages"][0]["from"]
                text = message["value"]["messages"][0]["text"]["body"]

                # Generar respuesta con Gemini AI
                response = genai.chat(messages=[{"role": "user", "content": text}])
                reply = response.last.text

                # Enviar respuesta a WhatsApp
                send_whatsapp_message(phone, reply)

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
