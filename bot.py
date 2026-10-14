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
def home(): return "OK"
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

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Assalomu alaykum! 👋\n\n"
        "Xush kelibsiz!\n\n"
        "Quyidagi menyudan tanlang 👇"
    )
    bot.send_message(message.chat.id, text, reply_markup=start_menu())

@bot.message_handler(func=lambda m: m.text and "Doctor Ali" in m.text)
def doctor_ali(message):
    try:
        if os.path.exists("ali_choy.jpg"):
            with open("ali_choy.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo, caption="DOCTOR ALI HEALTH TEA")
    except: pass
    bot.send_message(message.chat.id, "Narxi: 550,000 so'm\n\nQuyidagi menyudan tanlang 👇", reply_markup=choy_menu())

# TO'LIQ TARKIB - ESKI YAXSHI ISHLAGAN VARIANT QAYTARILDI
@bot.message_handler(func=lambda m: m.text and "Tarkib" in m.text)
def tarkib(message):
    text = (
        "🌿 *ALI HEALTH TEA - To'liq tarkibi va xususiyati:*\n\n"
        "🍃 *Tarkibida:*\n"
        "• Zanjabil, dolchin, qizilmiya\n"
        "• Moychechak, yalpiz, karkade\n"
        "• Tabiiy giyohlar aralashmasi\n\n"
        "💚 *Foydalari:*\n"
        "✅ Oshqozon yarasi, gastrit\n"
        "✅ Jigar yog' bosishi, jig'ildon qaynashi\n"
        "✅ Ichaklarni tozalash, qabziyat\n"
        "✅ Safro haydash, ishtaha ochish\n\n"
        "☕ *Ichish tartibi:*\n"
        "Kuniga 1 mahal ovqatdan 30 daqiqa oldin\n"
        "40 kunlik kurs - 40 ta ipak qopcha\n\n"
        "💰 *Narxi: 550,000 so'm*\n"
        "🚚 Yetkazib berish bepul!"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=choy_menu())

# MIJOZLAR FIKRI - VIDEO QO'SHILDI
@bot.message_handler(func=lambda m: m.text and "Mijozlar" in m.text)
def otziv(message):
    bot.send_message(message.chat.id, "💚 Mijozlarimiz fikri:")
    try:
        if os.path.exists("otziv1.mp4"):
            with open("otziv1.mp4", "rb") as video:
                bot.send_video(message.chat.id, video, caption="Mijozimizning haqiqiy natijasi! 👇")
        else:
            bot.send_message(message.chat.id, "Video topilmadi, fayl nomi otziv1.mp4 bo'lishi kerak")
    except Exception as e:
        bot.send_message(message.chat.id, f"Xato: {e}")
    bot.send_message(message.chat.id, "Tanlang 👇", reply_markup=choy_menu())

@bot.message_handler(func=lambda m: m.text and "Buyurtma" in m.text)
def buyurtma(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("📱 Raqamni yuborish", request_contact=True))
    bot.send_message(message.chat.id, "📱 Raqamingizni yuboring:", reply_markup=markup)
    bot.register_next_step_handler(message, get_contact)

def get_contact(message):
    phone = message.contact.phone_number if message.contact else message.text
    bot.send_message(message.chat.id, "✅ Rahmat! Qabul qilindi! Tez orada bog'lanamiz!", reply_markup=start_menu())
    try:
        bot.send_message(ADMIN_ID, f"🔔 YANGI BUYURTMA!\n📞 {phone}\n👤 {message.from_user.first_name}")
    except: pass

@bot.message_handler(func=lambda m: m.text and "Orqaga" in m.text)
def orqaga(message):
    start(message)

keep_alive()
bot.infinity_polling()
