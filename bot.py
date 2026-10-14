import os
import threading
from flask import Flask
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN yo'q!")

bot = telebot.TeleBot(TOKEN)

# Render port ochishi uchun kichik web server
app = Flask(__name__)
@app.route('/')
def home():
    return "Doctor Ali bot ishlayapti!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("☕ Doctor Ali choyi")
    bot.send_message(m.chat.id, "Assalomu alaykum! Bot ishga tushdi ✅", reply_markup=markup)

@bot.message_handler(func=lambda m: "Doctor Ali" in m.text)
def product(m):
    bot.send_message(m.chat.id, "☕ Doctor Ali choyi\n💰 550,000 so'm\n🚚 Yetkazib berish bepul\n\nBuyurtma uchun tel raqamingizni yozing!")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot polling boshlandi...")
    bot.infinity_polling()
