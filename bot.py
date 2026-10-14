import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 1271938077
bot = telebot.TeleBot(TOKEN)

app = Flask('')
@app.route('/')
def home(): return "Bot ishlayapti!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("☕ Doctor Ali choyi")
    return markup

def choy_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Tarkib va xususiyati", "Mijozlar fikri")
    markup.add("🛒 Buyurtma berish")
    markup.add("⬅️ Orqaga")
    return markup

# START - FAQAT SALOM, CHOY HAQIDA YO'Q!
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Assalomu alaykum! 👋\n\n"
        "Xush kelibsiz!\n\n"
        "Quyidagi menyudan tanlang 👇"
    )
    bot.send_message(message.chat.id, text, reply_markup=start_menu())

# DOCTOR ALI CHOYI BOSILGANDA
@bot.message_handler(func=lambda m: m.text and "Doctor Ali" in m.text)
def doctor_ali(message):
    try:
        if os.path.exists("ali_choy.jpg"):
            with open("ali_choy.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo)
    except: pass

    bot.send_message(message.chat.id, "Narxi: 550,000 so'm\n\nQuyidagi menyudan tanlang 👇", reply_markup=choy_menu())

# TARKIB
@bot.message_handler(func=lambda m: m.text and "Tarkib" in m.text)
def tarkib(message):
    text = (
        "🌿 *ALI HEALTH TEA - Tarkibi:*\n\n"
        "✅ 40 ta ipak qopcha (40 kunlik kurs)\n"
        "✅ 100% tabiiy\n"
        "✅ Oshqozon, jigar, ichaklar uchun\n\n"
        "Narxi: 550,000 so'm"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=choy_menu())

# MIJOZLAR FIKRI - VIDEO
@bot.message_handler(func=lambda m: m.text and "Mijozlar" in m.text)
def otziv(message):
    bot.send_message(message.chat.id, "Mijozlar fikri 👇")
    try:
        if os.path.exists("otziv1.mp4"):
            bot.send_chat_action(message.chat.id, 'upload_video')
            with open("otziv1.mp4", 'rb') as video:
                bot.send_video(message.chat.id, video, caption="💚 Mijozimiz fikri!")
    except Exception as e:
        print(e)
    bot.send_message(message.chat.id, "Tanlang 👇", reply_markup=choy_menu())

@bot.message_handler(func=lambda m: m.text and "Buyurtma" in m.text)
def buyurtma(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("📱 Raqamni yuborish", request_contact=True))
    bot.send_message(message.chat.id, "📱 Raqamingizni yuboring:", reply_markup=markup)
    bot.register_next_step_handler(message, get_contact)

def get_contact(message):
    phone = message.contact.phone_number if message.contact else message.text
    bot.send_message(message.chat.id, "✅ Rahmat! Buyurtmangiz qabul qilindi!", reply_markup=start_menu())
    try:
        bot.send_message(ADMIN_ID, f"🔔 YANGI BUYURTMA!\n📞 {phone}\n👤 {message.from_user.first_name}")
    except: pass

@bot.message_handler(func=lambda m: m.text and "Orqaga" in m.text)
def orqaga(message):
    start(message)

keep_alive()
bot.infinity_polling()
