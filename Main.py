import os
import telebot
from google import genai

TELEGRAM_TOKEN = ""9237007544:AAEWE4SaHre7RFwHOyYXlKGmHazVti5zkNE"
GEMINI_API_KEY = ""AQ.Ab8RN6KeK26uBn50mEE31aKgfEoaRJ8hUbeRGIugSJPcLwe_AA"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

bot.infinity_polling()
