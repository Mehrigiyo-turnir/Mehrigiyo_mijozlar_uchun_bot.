import telebot
from telebot import types

TOKEN = "SIZ_OLGAN_TOKENNI_SHU_YERGA_QOYING"
bot = telebot.TeleBot(TOKEN)

TARKIB_FOYDA = """
Таркиби: 25 хил табиий гиёҳ
Таркиби: атиргул, астра, гулхайри, қора андиз, мингбарг, иван-чой, зайтун, папайя, лаванда, тол, зубтурум, гуава, оқ қайин, зарчава, қизилмия, эхинацея, фундук, тоғжамбил, тоғрайҳон, сано, лимонўт, маврак, розмарин, чаканда, момақаймоқ.

🌿 FOYDASI (siz tashlagan jadvaldan):
1. Atirgul - Yurak, davleniya, infarkt, insult
2. Lavanda - Asab, uyqu, davleniya
3. Papaya - Ostexondroz, Grija, Bo'g'imlar
4. Momaqaymoq - Rak, onkologiya
5. Qizilmiya - Astma, Bronxit, Allergiya, Yo'tal
6. Exinatseya - Immunitet
7. Limon o'ti - Oshqozon, ishtaha
8. Gulxayri - Nafas yo'llari, Oshqozon ichak
9. Mingbarg - Yaralarni bitirish, qandli diabet
10. Tog' rayxoni - Jigar, buyrak
... va boshqa 15 xil giyoh.
To'liq 25 xil 100% tabiiy.
"""

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton("☕ Doctor Ali choyi"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "Assalomu alaykum! 💛\nDoctor Ali shifo choylari botiga xush kelibsiz!\n\nPastdagi tugmani bosing 👇",
        reply_markup=main_menu())

@bot.message_handler(func=lambda m: "Doctor Ali choyi" in m.text)
def product(message):
    inline = types.InlineKeyboardMarkup(row_width=1)
    inline.add(
        types.InlineKeyboardButton("🌿 Tarkibi va foydasi", callback_data="tarkib"),
        types.InlineKeyboardButton("💬 Mijozlar fikri", callback_data="otziv"),
        types.InlineKeyboardButton("📦 Buyurtma berish", callback_data="buyurtma")
    )
    caption = "☕ *Doctor Ali choyi*\n\n💰 *Narxi: 550,000 so'm*\n🚚 Yetkazib berish bepul\n🌿 25 xil tabiiy giyoh"
    try:
        with open('product.jpg', 'rb') as f:
            bot.send_photo(message.chat.id, f, caption=caption, reply_markup=inline, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, caption, reply_markup=inline, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: True)
def cb(call):
    if call.data == "tarkib":
        bot.send_message(call.message.chat.id, TARKIB_FOYDA)
    elif call.data == "otziv":
        bot.send_message(call.message.chat.id, "💬 Mijozlar video otzivlari tez orada shu yerda bo'ladi.")
    elif call.data == "buyurtma":
        bot.send_message(call.message.chat.id, "📦 Buyurtma uchun telefon raqamingizni yozib qoldiring!\nNarxi: 550,000 so'm")

bot.infinity_polling()
