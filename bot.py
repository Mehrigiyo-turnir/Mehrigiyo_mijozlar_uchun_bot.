import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 1271938077
bot = telebot.TeleBot(TOKEN)

# Keep Alive
app = Flask('')
@app.route('/')
def home(): return "Bot ishlayapti!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    Thread(target=run).start()

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("☕ Doctor Ali choyi")
    markup.add("Tarkib va xususiyati", "Mijozlar fikri")
    markup.add("🛒 Buyurtma berish")
    return markup

def order_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("📱 Raqamni yuborish", request_contact=True))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Assalomu alaykum! 👋\n\n"
        "🌿 *DOCTOR ALI HEALTH TEA* ga xush kelibsiz!\n\n"
        "Oshqozon, jigar va ichaklarni tozalovchi tabiiy choy.\n"
        "40 kunlik davolash kursi.\n\n"
        "💰 Narxi: 550,000 so'm\n"
        "🚚 Yetkazib berish bepul!\n\n"
        "Quyidagi menyudan tanlang 👇"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# TARKIB - 2 ta nomga ham javob beradi
@bot.message_handler(func=lambda m: m.text and ("Tarkib" in m.text or "Mahsulot" in m.text or "Doctor Ali" in m.text))
def tarkib(message):
    # Rasmni yuborish
    try:
        if os.path.exists("ali_choy.jpg"):
            with open("ali_choy.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo, caption="DOCTOR ALI HEALTH TEA - PREMIUM")
    except: pass

    text = (
        "🌿 *Tarkibi va xususiyati:*\n\n"
        "✅ 40 ta ipak qopcha (40 kunlik kurs)\n"
        "✅ 100% tabiiy giyohlar\n"
        "✅ Oshqozon yarasi, gastrit uchun\n"
        "✅ Jigar yog' bosishi, ichaklar uchun\n\n"
        "💰 Narxi: 550,000 so'm\n"
        "🚚 Yetkazib berish bepul!"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# MIJOZLAR FIKRI - VIDEO BILAN
@bot.message_handler(func=lambda m: m.text and "Mijozlar" in m.text)
def mijozlar(message):
    bot.send_message(message.chat.id, "Mijozlarimizning haqiqiy fikri 👇")
    try:
        # Video yuborish
        video_path = "otziv1.mp4"
        if os.path.exists(video_path):
            bot.send_chat_action(message.chat.id, 'upload_video')
            with open(video_path, 'rb') as video:
                bot.send_video(
                    message.chat.id,
                    video,
                    caption="💚 DOCTOR ALI - Mijozimiz natijasi! Oshqozon uchun juda foydali!"
                )
        else:
            bot.send_message(message.chat.id, "Video tez orada yuklanadi!")
    except Exception as e:
        print(f"Video xato: {e}")
        bot.send_message(message.chat.id, f"Video yuborishda xato, lekin tez orada to'g'rilaymiz!")

    bot.send_message(message.chat.id, "Buyurtma berishni xohlaysizmi? 👇", reply_markup=main_menu())

# BUYURTMA
@bot.message_handler(func=lambda m: m.text and "Buyurtma" in m.text)
def buyurtma(message):
    bot.send_message(message.chat.id, "📱 Iltimos raqamingizni yuboring:", reply_markup=order_markup())
    bot.register_next_step_handler(message, get_contact)

def get_contact(message):
    phone = message.contact.phone_number if message.contact else message.text
    bot.send_message(message.chat.id, "✅ Rahmat! Buyurtmangiz qabul qilindi!\nTez orada operator bog'lanadi!", reply_markup=main_menu())
    try:
        bot.send_message(ADMIN_ID, f"🔔 YANGI BUYURTMA!\n📞 {phone}\n👤 {message.from_user.first_name}\n🆔 {message.from_user.id}")
    except: pass

keep_alive()
print("Bot ishga tushdi...")
bot.infinity_polling()
