import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 1271938077
bot = telebot.TeleBot(TOKEN)

# Keep Alive - Render uxlatmasligi uchun
app = Flask('')
@app.route('/')
def home(): return "Bot ishlayapti!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("☕ Doctor Ali choyi")
    return markup

def choy_ostidagi_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Tarkib va xususiyati", "Mijozlar fikri")
    markup.add("🛒 Buyurtma berish")
    markup.add("⬅️ Orqaga")
    return markup

# /START - FAQAT SALOM
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Assalomu alaykum! 👋\n\n"
        "🌿 ALI HEALTH TEA ga xush kelibsiz!\n\n"
        "Oshqozon, jigar va ichaklarni tozalovchi tabiiy choy.\n"
        "40 kunlik davolash kursi - 40 ta ipak qopcha.\n\n"
        "Narxi: 550,000 so'm\n\n"
        "Quyidagi menyudan tanlang 👇"
    )
    bot.send_message(message.chat.id, text, reply_markup=start_menu())

# DOCTOR ALI CHOYI BOSILGANDA - RASIM + NARX + 2 KNOPKA
@bot.message_handler(func=lambda m: m.text and "Doctor Ali choyi" in m.text)
def doctor_ali(message):
    try:
        if os.path.exists("ali_choy.jpg"):
            with open("ali_choy.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo, caption="550,000 so'm")
        elif os.path.exists("ali_choy.jpeg"):
            with open("ali_choy.jpeg", "rb") as photo:
                bot.send_photo(message.chat.id, photo, caption="550,000 so'm")
        else:
            bot.send_message(message.chat.id, "☕ DOCTOR ALI HEALTH TEA\n💰 550,000 so'm")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "☕ DOCTOR ALI HEALTH TEA\n💰 550,000 so'm")

    bot.send_message(
        message.chat.id,
        "Tanlang 👇",
        reply_markup=choy_ostidagi_menu()
    )

# TARKIB VA XUSUSIYATI
@bot.message_handler(func=lambda m: m.text and "Tarkib" in m.text)
def tarkib(message):
    text = (
        "🌿 *Tarkibi va xususiyati:*\n\n"
        "✅ 40 ta ipak qopcha (40 kunlik kurs)\n"
        "✅ 100% tabiiy giyohlar\n"
        "✅ Oshqozon yarasi, gastrit, ichaklar\n"
        "✅ Jigar yog' bosishi, safro uchun\n\n"
        "Ichish tartibi: kuniga 1 mahal ovqatdan 30 daqiqa oldin\n\n"
        "💰 Narxi: 550,000 so'm\n"
        "🚚 Yetkazib berish bepul!"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=choy_ostidagi_menu())

# MIJOZLAR FIKRI - VIDEO OTZIV
@bot.message_handler(func=lambda m: m.text and "Mijozlar" in m.text)
def otziv(message):
    bot.send_message(message.chat.id, "Mijozlarimiz fikri 👇")
    try:
        if os.path.exists("otziv1.mp4"):
            bot.send_chat_action(message.chat.id, 'upload_video')
            with open("otziv1.mp4", 'rb') as video:
                bot.send_video(
                    message.chat.id,
                    video,
                    caption="💚 Mijozimizning haqiqiy fikri! ALI HEALTH TEA natijasi!"
                )
        else:
            bot.send_message(message.chat.id, "Video yuklanmoqda...")
    except Exception as e:
        print(f"Video xato: {e}")
        bot.send_message(message.chat.id, "Video yuborishda xatolik, tez orada to'g'rilaymiz!")
    
    bot.send_message(message.chat.id, "Buyurtma berasizmi?", reply_markup=choy_ostidagi_menu())

# BUYURTMA
@bot.message_handler(func=lambda m: m.text and "Buyurtma" in m.text)
def buyurtma(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("📱 Raqamni yuborish", request_contact=True))
    bot.send_message(message.chat.id, "📱 Raqamingizni yuboring:", reply_markup=markup)
    bot.register_next_step_handler(message, get_contact)

def get_contact(message):
    phone = message.contact.phone_number if message.contact else message.text
    bot.send_message(message.chat.id, "✅ Rahmat! Buyurtmangiz qabul qilindi!\nTez orada operator bog'lanadi!", reply_markup=start_menu())
    try:
        bot.send_message(ADMIN_ID, f"🔔 YANGI BUYURTMA!\n📞 {phone}\n👤 {message.from_user.first_name}")
    except: pass

@bot.message_handler(func=lambda m: m.text and "Orqaga" in m.text)
def orqaga(message):
    start(message)

keep_alive()
bot.infinity_polling()
