import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 1271938077
bot = telebot.TeleBot(BOT_TOKEN)

# VIDEO FILE_ID - KEYIN BU YERGA QO'YASIZ
VIDEO_FILE_ID = ""

app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# 1 - VIDEO FILE_ID OLISH - MARKDOWN YO'Q, XATOSIZ!
@bot.message_handler(content_types=['video', 'document'])
def video_id_olish(message):
    try:
        if message.content_type == 'video':
            file_id = message.video.file_id
        else:
            file_id = message.document.file_id
        
        bot.send_message(message.chat.id, "✅ FILE_ID OLINDI! Pastdagi kodni nusxalab oling:")
        bot.send_message(message.chat.id, file_id)
        print(f"FILE_ID: {file_id}")
    except Exception as e:
        print(f"Video xato: {e}")

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
        bot.send_message(message.chat.id, "Rasm topilmadi! ali_choy.jpg ni GitHub ga yuklang")

@bot.callback_query_handler(func=lambda call: call.data == "tarkib")
def tarkib_info(call):
    bot.answer_callback_query(call.id)
    text = (
        "🍃 Doctor Ali choyi - 25 xil tabiiy o't!\n\n"
        "1. Atirgul - Yurak, davleniya, infarkt, insult\n"
        "2. Lavanda - Asab, uyqu, davleniya\n"
        "3. Papaya - Ostexondroz, Grija, Bo'g'imlar\n"
        "4. Momaqaymoq - Rak, onkologiya\n"
        "5. Qizilmiya - Astma, Bronxit, Allergiya\n"
        "6. Exinatseya - Immunitet\n"
        "7. Limon o'ti - Oshqozon, ishtaha\n"
        "8. Gulxayri - Nafas yo'llari\n"
        "9. Mingbarg - Yara, diabet\n"
        "10. Tog' rayxoni - Jigar, buyrak\n"
        "11. Tog' jambili - Xotira, uyqu\n"
        "12. Funduk - Davleniya, varikoz\n"
        "13. Zarchava - Qon tozalash\n"
        "14. Guava - Limfa, immunitet\n"
        "15. Astra - Nafas yo'llari\n"
        "16. Qora andiz - Yo'tal, Gripp\n"
        "17. Ivan choy - Prostatit, quvvat\n"
        "18. Zaytun - Infeksiya\n"
        "19. Oq qayin - Gijja\n"
        "20. Sano - Qabziyat\n"
        "21. Mavrak - Tomoq, diabet\n"
        "22. Rozmarin - O't tosh, ko'z\n"
        "23. Chakanda - Gemaroy, teri\n"
        "24. Tol - Qon suyultirish\n"
        "25. Zubturum - Nafas, immunitet\n\n"
        "✅ 100% tabiiy\n"
        "📦 40 ta ipak qopcha\n"
        "⏳ 40 kunlik\n"
        "💰 550,000 so'm"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="buyurtma"))
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

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
            print(f"Video yuborish xato: {e}")
    bot.send_message(call.message.chat.id, "💬 Mijozlarimiz fikri tez orada!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "buyurtma")
def buyurtma_start(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "📞 Telefon raqamingizni yozing:\nMasalan: +998 90 123 45 67")

@bot.message_handler(func=lambda m: m.text is not None and len(m.text) >= 9)
def qabul_qilish(message):
    if not any(x in message.text for x in ['998', '+', '90', '91', '93', '94', '97', '88']):
        return
    bot.send_message(message.chat.id, "✅ Rahmat! Buyurtmangiz qabul qilindi!\nTez orada siz bilan bog'lanamiz!")
    try:
        username = f"@{message.from_user.username}" if message.from_user.username else ""
        matn = f"🔔 YANGI BUYURTMA!\nIsmi: {message.from_user.first_name}\nTel: {message.text}\n{username}\nID: {message.from_user.id}\nMahsulot: Doctor Ali choyi"
        bot.send_message(ADMIN_ID, matn)
    except Exception as e:
        print(f"Admin xato: {e}")

keep_alive()
bot.infinity_polling()
