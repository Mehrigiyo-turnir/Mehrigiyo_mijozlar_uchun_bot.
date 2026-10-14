import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 1271938077
bot = telebot.TeleBot(BOT_TOKEN)

VIDEO_FILE_ID = ""  # BU YERGA KEYIN FILE_ID QO'YASIZ

app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# 1-O'RINDA - VIDEO HANDLER - ENG TEPA!
@bot.message_handler(content_types=['video', 'document'])
def video_id_olish(message):
    try:
        if message.content_type == 'video':
            file_id = message.video.file_id
        else:
            file_id = message.document.file_id
        bot.send_message(message.chat.id, f"✅ FILE_ID OLINDI:\n\n`{file_id}`", parse_mode="Markdown")
        print(f"!!! FILE_ID TOPILDI: {file_id} !!!")
    except Exception as e:
        print(f"Video xato: {e}")
        bot.send_message(message.chat.id, f"Xato: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("☕ Doctor Ali choyi"))
    bot.send_message(message.chat.id, "Assalomu alaykum! Mahsulotni tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "☕ Doctor Ali choyi")
def choy_korsat(message):
    try:
        with open('ali_choy.jpg', 'rb') as photo:
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("Tarkib va xususiyati", callback_data="tarkib"),
                types.InlineKeyboardButton("Mijozlar fikri", callback_data="fikr")
            )
            bot.send_photo(message.chat.id, photo, caption="550,000 so'm", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "Rasm topilmadi!")

@bot.callback_query_handler(func=lambda call: call.data == "tarkib")
def tarkib_info(call):
    bot.answer_callback_query(call.id)
    text = (
        "🍃 *Doctor Ali choyi - 25 xil tabiiy o't!*\n\n"
        "1️⃣ *Atirgul* — Yurak, davleniya\n"
        "2️⃣ *Lavanda* — Asab, uyqu\n"
        "3️⃣ *Papaya* — Ostexondroz, Grija\n"
        "4️⃣ *Momaqaymoq* — Rak, onkologiya\n"
        "5️⃣ *Qizilmiya* — Astma, Bronxit\n"
        "6️⃣ *Exinatseya* — Immunitet\n"
        "7️⃣ *Limon o'ti* — Oshqozon\n"
        "8️⃣ *Gulxayri* — Nafas yo'llari\n"
        "9️⃣ *Mingbarg* — Diabet\n"
        "🔟 *Tog' rayxoni* — Jigar, buyrak\n"
        "1️⃣1️⃣ *Tog' jambili* — Xotira\n"
        "1️⃣2️⃣ *Funduk* — Davleniya\n"
        "1️⃣3️⃣ *Zarchava* — Qon tozalash\n"
        "1️⃣4️⃣ *Guava* — Limfa\n"
        "1️⃣5️⃣ *Astra* — Nafas yo'llari\n"
        "1️⃣6️⃣ *Qora andiz* — Yo'tal\n"
        "1️⃣7️⃣ *Ivan choy* — Prostatit\n"
        "1️⃣8️⃣ *Zaytun* — Infeksiya\n"
        "1️⃣9️⃣ *Oq qayin* — Gijja\n"
        "2️⃣0️⃣ *Sano* — Qabziyat\n"
        "2️⃣1️⃣ *Mavrak* — Tomoq, diabet\n"
        "2️⃣2️⃣ *Rozmarin* — O't tosh\n"
        "2️⃣3️⃣ *Chakanda* — Gemaroy\n"
        "2️⃣4️⃣ *Tol* — Qon suyultirish\n"
        "2️⃣5️⃣ *Zubturum* — Immunitet\n\n"
        "✅ 100% tabiiy - 40 ta ipak qopcha - 40 kunlik - 550,000 so'm"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="buyurtma"))
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "fikr")
def mijoz_fikri(call):
    bot.answer_callback_query(call.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="buyurtma"))
    if VIDEO_FILE_ID:
        try:
            bot.send_video(call.message.chat.id, VIDEO_FILE_ID, caption="💬 Mijozlarimiz fikri:", supports_streaming=True, reply_markup=markup)
            return
        except Exception as e:
            print(e)
    bot.send_message(call.message.chat.id, "💬 Mijozlarimiz fikri tez orada!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "buyurtma")
def buyurtma_start(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "📞 Telefon raqamingizni yozing:")

@bot.message_handler(func=lambda m: m.text is not None and len(m.text) >= 9 and any(x in m.text for x in ['998', '+']))
def qabul_qilish(message):
    bot.send_message(message.chat.id, "✅ Rahmat! Buyurtmangiz qabul qilindi!")
    try:
        username = f"@{message.from_user.username}" if message.from_user.username else ""
        matn = f"🔔 YANGI BUYURTMA!\nIsmi: {message.from_user.first_name}\nTel: {message.text}\n{username}\nID: {message.from_user.id}"
        bot.send_message(ADMIN_ID, matn)
    except Exception as e:
        print(e)

keep_alive()
bot.infinity_polling()
