import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import telebot
from google import genai

TELEGRAM_TOKEN = "9237007544:AAET9a2UfcAp5SvnGYmIwB_EJ9iC2XbAFYQ"
GEMINI_API_KEY = "AQ.Ab8RN6I4uZVJ3vIbzAaTzhWa2m685EGEVGuR_GQOeyNI5Stttg"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        pass


def start_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=message.text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")


if __name__ == "__main__":
    threading.Thread(target=start_health_server, daemon=True).start()
    bot.infinity_polling()
