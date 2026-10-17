import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 1271938077
bot = telebot.TeleBot(BOT_TOKEN)

VIDEO_FILE_ID = "BAACAgIAAxkBAANaas9MA9e_BNu9Pg2fqLHekHxFSOcAAiukAAJXboFKacmQsAP-vEo9BA"
ELIXIR_VIDEO_FILE_ID = "BAACAgIAAxkBAAOoatB3W-M6AQAB-6O4fUsizlhIsVmdAAIErgACqe2BShIC0a6dfwiQPQQ"
KREM_VIDEO_ID_1 = "BAACAgIAAxkBAAOPatB1BvqP93UPUc1bo_1C76R2z4MAAuitAAKp7YFK0a4Bv_IxqLw9BA"
KREM_VIDEO_ID_2 = "BAACAgIAAxkBAAOSatB1WPGI2rzUQ5AfPBqIgYbes0IAAu-tAAKp7YFK6OdSbCMR1Po9BA"
ALATOO_VIDEO_ID = "BAACAgIAAxkBAAPLatNALr7Mt37CDOrLPC-CFaZQrusAAtiDAAJcn_FIMmbgpjqxcis9BA"
ALATOO_FIKR_VIDEO_ID = "BAACAgIAAxkBAAPXatNFhhrjOwLUMGuHBRvlHPaEl84AAhutAAKMk6FKYpOKucWtLug9BA"

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
    markup.add(types.KeyboardButton("Doctor Ali Elixir Premium"))
    markup.add(types.KeyboardButton(" Doctor Ali kremi"))
    markup.add(types.KeyboardButton("🏔 Alatoo"))
    bot.send_message(message.chat.id, "Assalomu alaykum! Mahsulotni tanlang:", reply_markup=markup)

# ===== ALATOO =====
@bot.message_handler(func=lambda m: m.text == "🏔 Alatoo")
def alatoo_korsat(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🥤 Ichilish tartibi", callback_data="alatoo_ichish"),
        types.InlineKeyboardButton("💬 Mijozlar fikri", callback_data="alatoo_fikr")
    )
    try:
        bot.send_video(message.chat.id, ALATOO_VIDEO_ID, caption="🏔 Alatoo\n💰 1.370.000 so'm", supports_streaming=True, reply_markup=markup)
    except Exception as e:
        print(f"ALATOO VIDEO XATO: {e}")
        bot.send_message(message.chat.id, "🏔 Alatoo\n💰 1.370.000 so'm", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "alatoo_ichish")
def alatoo_ichish(call):
    bot.answer_callback_query(call.id)
    text = (
        "🥤 Ichilish tartibi:\n\n"
        "3 yoshdan 7 yoshgacha - 3 mahal 1 choy qoshiqdan\n"
        "7 yoshdan 12 yoshgacha - 1 osh qoshiqdan\n"
        "12 yoshdan kattalar - 2 osh qoshiqdan, 3 mahal"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="alatoo_buyurtma"))
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "alatoo_fikr")
def alatoo_fikr(call):
    bot.answer_callback_query(call.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="alatoo_buyurtma"))
    try:
        bot.send_video(call.message.chat.id, ALATOO_FIKR_VIDEO_ID, caption="💬 Mijozlarimiz fikri - Alatoo", supports_streaming=True, reply_markup=markup)
    except Exception as e:
        print(f"ALATOO FIKR VIDEO XATO: {e}")
        bot.send_message(call.message.chat.id, "💬 Mijozlar fikri tez orada!", reply_markup=markup)

# ===== CHOY =====
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
        "🍃 Doctor Ali choyi - 25 xil tabiiy giyoh!\n\n"
        "1️⃣ Atirgul — Yurak, davleniya, infarkt, insult\n"
        "2️⃣ Lavanda — Asab, uyqu, davleniya\n"
        "3️⃣ Papaya — Ostexondroz, Grija, Bo'g'imlar, Poleartirt\n"
        "4️⃣ Momaqaymoq — Rak, onkologiya\n"
        "5️⃣ Qizilmiya — Astma, Bronxit, Allergiya, Yo'tal, Istma\n"
        "6️⃣ Exinatseya — Immunitet\n"
        "7️⃣ Limon giyohi — Oshqozon, ishtaha\n"
        "8️⃣ Gulxayri — Nafas yo'llari, Oshqozon ichak\n"
        "9️⃣ Mingbarg — Yaralarni bitirishda, qandli diabet\n"
        "🔟 Tog' rayhoni — Jigar, ishtaha, buyrak\n"
        "1️⃣1️⃣ Tog' jambili — Xotira, uyqu, immunitet\n"
        "1️⃣2️⃣ Funduk — Davleniya, ortiqcha vazn, varikoz\n"
        "1️⃣3️⃣ Zarchava — Qon tozalashda, Revmatizmda\n"
        "1️⃣4️⃣ Guava — Limfa tizimiga, immunitet\n"
        "1️⃣5️⃣ Astra — Nafas yo'llari, Yaralarni bitirishda\n"
        "1️⃣6️⃣ Qora andiz — Yo'tal, Gripp, Istma\n"
        "1️⃣7️⃣ Ivan choy — Prostatit, quvvat, adenoma\n"
        "1️⃣8️⃣ Zaytun — Qondagi infeksiyaga\n"
        "1️⃣9️⃣ Oq qayin — Gijja\n"
        "2️⃣0️⃣ Sano — Qabziyat\n"
        "2️⃣1️⃣ Mavrak — Tomoq og'rig'i, qandli diabet\n"
        "2️⃣2️⃣ Rozmarin — O't tosh kasalligi, ko'z o'tkirlashishi\n"
        "2️⃣3️⃣ Chakanda — Gemaroy, teri kasalligi\n"
        "2️⃣4️⃣ Tol — Qon suyultirishda\n"
        "2️⃣5️⃣ Zubturum — Nafas yo'llari, immunitet\n\n"
        "✅ 100% tabiiy\n📦 40 ta ipak qopcha\n⏳ 40 kunlik muolaja\n💰 550,000 so'm"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="buyurtma"))
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "fikr")
def mijoz_fikri(call):
    bot.answer_callback_query(call.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="buyurtma"))
    try:
        bot.send_video(call.message.chat.id, VIDEO_FILE_ID, caption="💬 Mijozlarimiz fikri:", supports_streaming=True, reply_markup=markup)
    except:
        bot.send_message(call.message.chat.id, "💬 Mijozlarimiz fikri tez orada!", reply_markup=markup)

# ===== ELIXIR =====
@bot.message_handler(func=lambda m: m.text == "Doctor Ali Elixir Premium")
def elixir_korsat(message):
    try:
        with open('elixir_premium.jpg', 'rb') as photo:
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🌿 Tarkibi", callback_data="elixir_tarkib"),
                types.InlineKeyboardButton("💚 Foydasi", callback_data="elixir_foyda")
            )
            markup.add(
                types.InlineKeyboardButton("🥄 Ichish tartibi", callback_data="elixir_ichish"),
                types.InlineKeyboardButton("💬 Fikrlar", callback_data="elixir_fikr")
            )
            bot.send_photo(message.chat.id, photo, caption="Elixir Premium Sirobi\n💰 700,000 so'm (330gr x 2 dona)", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "elixir_premium.jpg rasmini yuklang!")

@bot.callback_query_handler(func=lambda call: call.data == "elixir_tarkib")
def elixir_tarkib(call):
    bot.answer_callback_query(call.id)
    text = (
        "Elixir Premium Sirobi - 22 xil meva va o'simliklar\n\n"
        "1️⃣ Anor va olma sharbati\n2️⃣ Tut\n3️⃣ Tarvuz\n4️⃣ Guava\n5️⃣ Papaya\n"
        "6️⃣ Do'lana\n7️⃣ Zarchva\n8️⃣ Zanjabil\n9️⃣ Rastaropsha\n🔟 Amarant\n"
        "1️⃣1️⃣ Zaytun\n1️⃣2️⃣ Ginko biloba\n1️⃣3️⃣ Kiprey\n1️⃣4️⃣ Goji\n1️⃣5️⃣ Igir\n"
        "1️⃣6️⃣ Oq qayin\n1️⃣7️⃣ Namatak\n1️⃣8️⃣ Selderey\n1️⃣9️⃣ Urmon yong'og'i\n"
        "2️⃣0️⃣ Chakanda\n2️⃣1️⃣ Exinatseya\n\n✅ 100% tabiiy\n📦 330gr x 2 dona"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="elixir_buyurtma"))
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "elixir_foyda")
def elixir_foyda(call):
    bot.answer_callback_query(call.id)
    text = (
        "💚 Foydali xususiyati:\n\n"
        "1️⃣ Ko'rish qobilyatini yaxshilaydi\n2️⃣ O'pka faolyatini yaxshilashda\n"
        "3️⃣ Jigarni tozalashda\n4️⃣ Buyrak faolyatini yaxshilashda\n"
        "5️⃣ Yurak qon-tomir kasalliklarini oldini oladi\n"
        "6️⃣ Organizmni qarishini sekinlashtiradi\n7️⃣ Yog'larni eritadi\n"
        "8️⃣ Xotira miya faolyatini yaxshilaydi\n9️⃣ Kuchli antioksidant hisoblanadi\n"
        "🔟 Bo'g'imlarni mustahkamlaydi\n1️⃣1️⃣ Saraton xavfini kamaytiradi\n"
        "1️⃣2️⃣ Prastata - jinsiy zaiflikni oldini oladi\n\n💰 700,000 so'm"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="elixir_buyurtma"))
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "elixir_ichish")
def elixir_ichish(call):
    bot.answer_callback_query(call.id)
    text = (
        "🥄 Ichish tartibi:\n\n"
        "👶 3 yoshdan 12 yoshgacha: 1 osh qoshiqdan\n"
        "🧑 12 yoshdan kattalar: 2 osh qoshiqdan\n"
        "Kunda 3 mahal\n\n💰 700,000 so'm"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="elixir_buyurtma"))
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "elixir_fikr")
def elixir_fikr(call):
    bot.answer_callback_query(call.id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="elixir_buyurtma"))
    try:
        bot.send_video(call.message.chat.id, ELIXIR_VIDEO_FILE_ID, caption="💬 Elixir Premium - Mijozlarimiz fikri\n💚 100% natural natija!", supports_streaming=True, reply_markup=markup)
    except Exception as e:
        print(f"ELIXIR VIDEO XATO: {e}")
        bot.send_message(call.message.chat.id, "💬 Mijozlar fikri tez orada!", reply_markup=markup)

# ===== KREM =====
@bot.message_handler(func=lambda m: m.text == " Doctor Ali kremi")
def krem_korsat(message):
    try:
        with open('doctor_ali_kremi.jpg', 'rb') as photo:
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("🌿 Tarkibi", callback_data="krem_tarkib"),
                types.InlineKeyboardButton("💚 Foydasi", callback_data="krem_foyda")
            )
            markup.add(
                types.InlineKeyboardButton("🖐 Qo'llanilishi", callback_data="krem_qollanish"),
                types.InlineKeyboardButton("💬 Fikrlar", callback_data="krem_fikr")
            )
            bot.send_photo(message.chat.id, photo, caption="Doctor Ali Rayhon Kremi\n💰 600,000 so'm (3 dona)", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "doctor_ali_kremi.jpg rasmini yuklang!")

@bot.callback_query_handler(func=lambda call: call.data == "krem_tarkib")
def krem_tarkib(call):
    bot.answer_callback_query(call.id)
    text = "🌿 Tarkibi:\n\n✅ Zanjabil ekstrakti\n✅ Lavanda efir moyi\n✅ Mentol\n✅ Kamfora\n✅ Mum\n\n✅ 100% tabiiy\n📦 3 dona\n💰 600,000 so'm"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="krem_buyurtma"))
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "krem_foyda")
def krem_foyda(call):
    bot.answer_callback_query(call.id)
    text = "💚 Foydali xususiyati:\n\n✔️ Qon aylanishini yaxshilashda\n✔️ Og'riqlarni yengillashtiradi\n✔️ Shamollash va yallig'lanishga qarshi\n\n🔹 Qaysi kasalliklarda:\n• Poliartrit\n• Artrit\n• Artroz\n• Grija\n• Asteaxandroz\n• Mushaklar spazmi\n• Shpora\n• Jarohatlardan keyingi tiklanish\n\n💰 600,000 so'm (3 dona)"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="krem_buyurtma"))
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "krem_qollanish")
def krem_qollanish(call):
    bot.answer_callback_query(call.id)
    text = "🖐 Qo'llanilishi:\n\nKunda 3 marotaba og'riqli joylarga surtiladi.\n\n💰 600,000 so'm (3 dona)"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="krem_buyurtma"))
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "krem_fikr")
def krem_fikr(call):
    bot.answer_callback_query(call.id)
    try:
        bot.send_video(call.message.chat.id, KREM_VIDEO_ID_1, caption="💬 Krem - Mijozlar fikri 1/2", supports_streaming=True)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="krem_buyurtma"))
        bot.send_video(call.message.chat.id, KREM_VIDEO_ID_2, caption="💬 Krem - Mijozlar fikri 2/2", supports_streaming=True, reply_markup=markup)
    except Exception as e:
        print(f"KREM VIDEO XATO: {e}")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="krem_buyurtma"))
        bot.send_message(call.message.chat.id, "💬 Mijozlar fikri tez orada!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["buyurtma", "elixir_buyurtma", "krem_buyurtma", "alatoo_buyurtma"])
def buyurtma_start(call):
    bot.answer_callback_query(call.id)
    if call.data == "buyurtma":
        turi = "Choy"
    elif call.data == "elixir_buyurtma":
        turi = "Elixir Premium"
    elif call.data == "alatoo_buyurtma":
        turi = "Alatoo"
    else:
        turi = "Doctor Ali kremi"
    bot.send_message(call.message.chat.id, f"📦 {turi} uchun\n📞 Telefon raqamingizni yozing:")

@bot.message_handler(func=lambda m: m.text is not None and len(m.text) >= 9)
def qabul_qilish(message):
    if not any(x in message.text for x in ['998', '+', '90', '91', '93', '94', '97', '88']):
        return
    bot.send_message(message.chat.id, "✅ Rahmat! Buyurtmangiz qabul qilindi!")
    try:
        username = f"@{message.from_user.username}" if message.from_user.username else ""
        matn = f"🔔 YANGI BUYURTMA!\nIsmi: {message.from_user.first_name}\nTel: {message.text}\n{username}\nID: {message.from_user.id}"
        bot.send_message(ADMIN_ID, matn)
    except Exception as e:
        print(e)

@bot.message_handler(content_types=['video', 'document'])
def video_update(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        file_id = message.video.file_id if message.content_type == 'video' else message.document.file_id
        bot.send_message(message.chat.id, "✅ Yangi FILE_ID:")
        bot.send_message(message.chat.id, file_id)
    except:
        pass

keep_alive()
bot.infinity_polling()
