from flask import Flask, request
from config import VERIFY_TOKEN
from whatsapp_api import send_whatsapp_message
from gemini_api import get_gemini_response

app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def verify():
    token_sent = request.args.get("hub.verify_token")
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid token", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    if "messages" in data["entry"][0]["changes"][0]["value"]:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        phone_number = message["from"]
        text = message["text"]["body"]

        response = get_gemini_response(text)
        send_whatsapp_message(phone_number, response)

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
