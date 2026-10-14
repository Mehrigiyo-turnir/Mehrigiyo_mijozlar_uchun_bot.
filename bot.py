import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 1271938077
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("☕ Doctor Ali choyi"))
    bot.send_message(message.chat.id, "Assalomu alaykum! Mahsulotni tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "☕ Doctor Ali choyi")
def choy_korsat(message):
    try:
        with open('ali_choy.jpg', 'rb') as photo:
            caption = "550,000 so'm"
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("Tarkib va xususiyati", callback_data="tarkib"),
                types.InlineKeyboardButton("Mijozlar fikri", callback_data="fikr")
            )
            bot.send_photo(message.chat.id, photo, caption=caption, reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "Rasm topilmadi!")

@bot.callback_query_handler(func=lambda call: call.data == "tarkib")
def tarkib_info(call):
    bot.answer_callback_query(call.id)
    text = (
        "🍃 *Doctor Ali choyi - 25 xil tabiiy o't!*\n\n"
        "1️⃣ *Atirgul* — Yurak, davleniya, infarkt, insult\n"
        "2️⃣ *Lavanda* — Asab, uyqu, davleniya\n"
        "3️⃣ *Papaya* — Ostexondroz, Grija, Bo'g'imlar, Poleartirt\n"
        "4️⃣ *Momaqaymoq* — Rak, onkologiya\n"
        "5️⃣ *Qizilmiya* — Astma, Bronxit, Allergiya, Yo'tal, Istma\n"
        "6️⃣ *Exinatseya* — Immunitet\n"
        "7️⃣ *Limon o'ti* — Oshqozon, ishtaha\n"
        "8️⃣ *Gulxayri* — Nafas yo'llari, Oshqozon ichak\n"
        "9️⃣ *Mingbarg* — Yaralarni bitirishda, qandli diabet\n"
        "🔟 *Tog' rayxoni* — Jigar, ishtaha, buyrak\n"
        "1️⃣1️⃣ *Tog' jambili* — Xotira, uyqu, immunitet\n"
        "1️⃣2️⃣ *Funduk* — Davleniya, ortiqcha vazn, varikoz\n"
        "1️⃣3️⃣ *Zarchava* — Qon tozalashda, Revmatizmda\n"
        "1️⃣4️⃣ *Guava* — Limfa tizimiga, immunitet\n"
        "1️⃣5️⃣ *Astra* — Nafas yo'llari, Yaralarni bitirishda\n"
        "1️⃣6️⃣ *Qora andiz* — Yo'tal, Gripp, Istma\n"
        "1️⃣7️⃣ *Ivan choy* — Prostatit, quvvat, adenoma\n"
        "1️⃣8️⃣ *Zaytun* — Qondagi infeksiyaga\n"
        "1️⃣9️⃣ *Oq qayin* — Gijja\n"
        "2️⃣0️⃣ *Sano* — Qabziyat\n"
        "2️⃣1️⃣ *Mavrak* — Tomoq og'rig'i, qandli diabet\n"
        "2️⃣2️⃣ *Rozmarin* — O't tosh kasalligi, ko'z o'tkirlashishi\n"
        "2️⃣3️⃣ *Chakanda* — Gemaroy, teri kasalligi\n"
        "2️⃣4️⃣ *Tol* — Qon suyultirishda\n"
        "2️⃣5️⃣ *Zubturum* — Nafas yo'llari, immunitet\n\n"
        "✅ 100% tabiiy\n"
        "📦 Qadoqida 40 ta ipak qopcha mavjud\n"
        "⏳ 40 kunlik licheniya\n"
        "💰 550,000 so'm"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="buyurtma"))
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# YANGILANGAN - ENDI VIDEO CHIQADI
@bot.callback_query_handler(func=lambda call: call.data == "fikr")
def mijoz_fikri(call):
    bot.answer_callback_query(call.id)
    try:
        if os.path.exists('otziv1.mp4'):
            with open('otziv1.mp4', 'rb') as video:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="buyurtma"))
                bot.send_video(call.message.chat.id, video, caption="💬 *Mijozlarimiz fikri:*", parse_mode="Markdown", reply_markup=markup)
                return
    except Exception as e:
        print(f"Video xato: {e}")
    
    bot.send_message(call.message.chat.id, "💬 *Mijozlarimiz fikri:*\n\nTez orada video otzivlar joylanadi!", parse_mode="Markdown")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="buyurtma"))
    bot.send_message(call.message.chat.id, "Buyurtma bering 👇", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "buyurtma")
def buyurtma_start(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "📞 Telefon raqamingizni yozing:\nMasalan: +998 90 123 45 67")

@bot.message_handler(func=lambda m: m.text and ('998' in m.text or m.text.startswith('+') or m.text.replace(' ','').isdigit()))
def qabul_qilish(message):
    if len(message.text) < 9:
        return
    bot.send_message(message.chat.id, "✅ Rahmat! Buyurtmangiz qabul qilindi!\nTez orada siz bilan bog'lanamiz!")
    try:
        username = f"@{message.from_user.username}" if message.from_user.username else "Username yo'q"
        matn = (
            f"🔔 *YANGI BUYURTMA!*\n\n"
            f"👤 Ismi: {message.from_user.first_name}\n"
            f"📞 Tel: {message.text}\n"
            f"💬 {username}\n"
            f"🆔 ID: {message.from_user.id}\n"
            f"📦 Mahsulot: Doctor Ali choyi - 40 ta ipak qopcha - 550,000 so'm\n"
            f"⏰ 40 kunlik licheniya"
        )
        bot.send_message(ADMIN_ID, matn, parse_mode="Markdown")
    except Exception as e:
        print(f"Admin ga yuborishda xato: {e}")

keep_alive()
bot.infinity_polling()
