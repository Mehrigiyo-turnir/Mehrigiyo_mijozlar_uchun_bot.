import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# --- SOZLAMALAR ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Render da Environment ga qo'ying!
ADMIN_ID = 123456789  # O'zingizni Telegram ID ni yozing ( @userinfobot dan oling )

bot = telebot.TeleBot(BOT_TOKEN)

# --- FLASK (Render uxlamasligi uchun) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- /start ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("☕ Doctor Ali choyi")
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! Bot ishga tushdi ✅\n\nMahsulotni tanlang:",
        reply_markup=markup
    )

# --- Doctor Ali choyi bosilganda: FAQAT RASM + NARX + 2 KNOPKA ---
@bot.message_handler(func=lambda m: m.text == "☕ Doctor Ali choyi")
def choy_korsat(message):
    try:
        # Rasm - GitHub da ali_choy.jpg nomi bilan turishi kerak
        with open('ali_choy.jpg', 'rb') as photo:
            caption = "550,000 so'm"
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("Tarkib va xususiyati", callback_data="tarkib"),
                types.InlineKeyboardButton("Mijozlar fikri", callback_data="fikr")
            )
            bot.send_photo(message.chat.id, photo, caption=caption, reply_markup=markup)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Rasm topilmadi! GitHub ga ali_choy.jpg ni yuklang!")

# --- TARKIB BOSILGANDA ---
@bot.callback_query_handler(func=lambda call: call.data == "tarkib")
def tarkib_info(call):
    bot.answer_callback_query(call.id)
    text = (
        "🍃 *Tarkib va xususiyati:*\n\n"
        "• Papaya bargi - organizmni tozalaydi\n"
        "• Romashka - asabni tinchlantiradi\n"
        "• Atirgul - immunitetni ko'taradi\n"
        "• Zira, yalpiz, qizilmiya va boshqa tabiiy o'tlar\n\n"
        "✅ 100% tabiiy\n"
        "✅ 20 ta filtr-paket, 50g\n"
        "✅ Yetkazib berish bepul"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="buyurtma"))
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# --- MIJOZLAR FIKRI BOSILGANDA (VIDEO) ---
@bot.callback_query_handler(func=lambda call: call.data == "fikr")
def mijoz_fikri(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "💬 *Mijozlarimiz fikri:*\n\nTez orada video otzivlar joylanadi!", parse_mode="Markdown")
    
    # --- VIDEO LAR KELGANDA SHU YERGA QO'SHILADI ---
    # Siz video tashlaganingizda men buni to'ldirib beraman:
    # bot.send_video(call.message.chat.id, open('video1.mp4', 'rb'), caption="Mijoz fikri 1")
    # bot.send_video(call.message.chat.id, open('video2.mp4', 'rb'), caption="Mijoz fikri 2")
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="buyurtma"))
    bot.send_message(call.message.chat.id, "Videolar yoqdimi? Buyurtma bering 👇", reply_markup=markup)

# --- BUYURTMA ---
@bot.callback_query_handler(func=lambda call: call.data == "buyurtma")
def buyurtma_start(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Buyurtma uchun telefon raqamingizni yozing:\nMasalan: +998 90 123 45 67")

@bot.message_handler(func=lambda m: m.text.startswith('+998') or m.text.startswith('998'))
def qabul_qilish(message):
    bot.send_message(message.chat.id, "✅ Rahmat! Tez orada siz bilan bog'lanamiz!")
    # Adminga xabar
    try:
        bot.send_message(ADMIN_ID, f"🔔 Yangi buyurtma!\n\nMijoz: {message.from_user.first_name}\nTel: {message.text}\nUsername: @{message.from_user.username}")
    except:
        pass

# --- ISHGA TUSHIRISH ---
keep_alive()
print("Bot ishga tushdi...")
bot.infinity_polling()
