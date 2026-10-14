import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
print("Token bor yo'qligi:", bool(TOKEN))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Bot ishladi ✅")

bot.infinity_polling()
