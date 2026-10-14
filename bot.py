import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 1271938077

bot = telebot.TeleBot(TOKEN)

# ----- Keep Alive (Render uxlatmasligi uchun) -----
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ----- Tugmalar -----
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🌿 Mahsulot haqida", "⭐ Mijozlar fikri")
    markup.add("🛒 Buyurtma berish")
    return markup

def order_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton("📱 Raqamni yuborish", request_contact=True))
    return markup

def buyurtma_tugmasi():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 Buyurtma berish")
    markup.add("🌿 Mahsulot haqida", "⭐ Mijozlar fikri")
    return markup

# ----- /start -----
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Assalomu alaykum! 👋\n\n"
        "🌿 *ALI HEALTH TEA* ga xush kelibsiz!\n\n"
        "Oshqozon, jigar va ichaklarni tozalovchi tabiiy choy.\n"
        "40 kunlik davolash kursi - 40 ta ipak qopcha.\n\n"
        "Narxi: 550,000 so'm\n\n"
        "Quyidagi menyudan tanlang 👇"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=main_menu())

# ----- Mahsulot haqida -----
@bot.message_handler(func=lambda m: m.text == "🌿 Mahsulot haqida")
def mahsulot(message):
    text = (
        "🌿 *ALI HEALTH TEA - Tarkibi:*\n\n"
        "✅ 40 ta ipak qopcha (40 kunlik kurs)\n"
        "✅ 100% tabiiy giyohlar\n"
        "✅ Oshqozon yarasi, gastrit, jigar yog' bosishi uchun\n\n"
        "💰 Narxi: 550,000 so'm\n"
        "🚚 Yetkazib berish bepul!\n\n"
        "Buyurtma berish uchun tugmani bosing 👇"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=buyurtma_tugmasi())

# ----- Mijozlar fikri - VIDEO BILAN -----
@bot.message_handler(func=lambda m: m.text == "⭐ Mijozlar fikri")
def mijozlar_fikri(message):
    bot.send_message(message.chat.id, "Mijozlarimizning haqiqiy fikri 👇\nIltimos kuting, video yuklanmoqda...")

    # Videoni yuborish (2 joydan qidiradi)
    video_sent = False
    for path in ["otziv1.mp4", "videos/otziv1.mp4", "otziv1.MP4"]:
        if os.path.exists(path):
            try:
                bot.send_chat_action(message.chat.id, 'upload_video')
                with open(path, 'rb') as video:
                    bot.send_video(
                        message.chat.id,
                        video,
                        caption="💚 *ALI HEALTH TEA* - Mijozimizning haqiqiy natijasi!\n\nOshqozon va jigar uchun juda foydali ekanligini aytmoqda!",
                        parse_mode="Markdown"
                    )
                video_sent = True
                break
            except Exception as e:
                print(f"Video xato: {e}")

    if not video_sent:
        bot.send_message(message.chat.id, "Video hali yuklanmadi, tez orada qo'shiladi!")

    bot.send_message(
        message.chat.id,
        "Siz ham sog'lig'ingizni tiklamoqchimisiz? 👇",
        reply_markup=buyurtma_tugmasi()
    )

# ----- Buyurtma berish -----
@bot.message_handler(func=lambda m: m.text == "🛒 Buyurtma berish")
def buyurtma(message):
    bot.send_message(
        message.chat.id,
        "📱 Iltimos telefon raqamingizni yuboring:\n\nTugmani bosing yoki raqamni yozing (+998...)",
        reply_markup=order_markup()
    )
    bot.register_next_step_handler(message, get_contact)

def get_contact(message):
    phone = None
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text

    if not phone:
        bot.send_message(message.chat.id, "Iltimos raqam yuboring!")
        return

    # Mijozga javob
    bot.send_message(
        message.chat.id,
        "✅ *Rahmat! Buyurtmangiz qabul qilindi!*\n\n"
        "Tez orada operatorimiz siz bilan bog'lanadi!\n"
        "🚚 Yetkazib berish bepul!",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

    # Sizga - ADMIN ga xabar
    try:
        admin_text = (
            f"🔔 *YANGI BUYURTMA!*\n\n"
            f"📞 Tel: {phone}\n"
            f"👤 Ismi: {message.from_user.first_name}\n"
            f"🆔 ID: {message.from_user.id}\n"
            f"🌿 Mahsulot: ALI HEALTH TEA\n"
            f"💰 Narxi: 550,000 so'm"
        )
        bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
    except Exception as e:
        print(f"Admin ga yuborishda xato: {e}")

# ----- Ishga tushirish -----
keep_alive()
print("Bot ishga tushdi...")
bot.infinity_polling()
