import telebot
from telebot import types

TOKEN = "8252134065:AAEAHlbftOBZ-z7iWmqbknOo9QQAUC4ijRo" 
bot = telebot.TeleBot(TOKEN)
ADMIN_ID =  282155346
# --- START ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🧮 Gilam m² hisoblash")
    markup.add("📦 Buyurtma berish")
    markup.add("📞 Aloqa")

    bot.send_message(
        message.chat.id,
        "Assalomu alaykum!\n"
        "G‘ijduvon Toza Gilam yuvish botiga xush kelibsiz 😊\n\n"
        "Kerakli bo‘limni tanlang 👇",
        reply_markup=markup
    )

# --- ALOQA ---
@bot.message_handler(func=lambda m: m.text == "📞 Aloqa")
def contact(message):
    bot.send_message(
        message.chat.id,
        "📞 Aloqa raqamlari:\n"
        "93 841 89 00\n"
        "90 614 26 73"
    )

# --- M2 HISOBLASH ---
@bot.message_handler(func=lambda m: m.text == "🧮 Gilam m² hisoblash")
def ask_size(message):
    bot.send_message(
        message.chat.id,
        "Gilamning ENI va UZUNLIGINI metrda yozing.\n"
        "Masalan: 2 3"
    )
    bot.register_next_step_handler(message, calculate_m2)

def calculate_m2(message):
    try:
        eni, uzunligi = map(float, message.text.split())
        m2 = eni * uzunligi
        narx = m2 * 10000  # 1 m² = 10000 so‘m (xohlasangiz o‘zgartiramiz) 

        bot.send_message(
            message.chat.id,
            f"📐 Gilam maydoni: {m2:.2f} m²\n"
            f"💰 Taxminiy narx: {int(narx)} so‘m"
        )
    except:
        bot.send_message(
            message.chat.id,
            "❌ Iltimos, to‘g‘ri yozing.\nMasalan: 2 3"
        )

# --- BUYURTMA ---
@bot.message_handler(func=lambda m: m.text == "📦 Buyurtma berish")
def order_start(message):
    bot.send_message(message.chat.id, "Ismingizni yozing:")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    name = message.text
    bot.send_message(message.chat.id, "Manzilingizni yozing:")
    bot.register_next_step_handler(message, get_address, name)

def get_address(message, name):
    address = message.text
    bot.send_message(message.chat.id,
 "Telefon raqamingizni yozing:")
    bot.register_next_step_handler(message, save_order, name, address)

def save_order(message, name, address):
    phone = message.text

    order_text = (
        f"🧾 YANGI BUYURTMA!\n\n"
        f"👤 Ism: {name}\n"
        f"🏠 Manzil: {address}\n"
        f"📞 Telefon: {phone}"
    )

    # Faylga yozish
    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(order_text + "\n---\n")

    # KLIENTGA javob
    bot.send_message(
        message.chat.id,
        "✅ Buyurtmangiz qabul qilindi!\n"
        "📞 G‘ijduvon Toza Gilam xodimlari tez orada siz bilan bog‘lanadi."
    )

    # SIZGA (ADMIN) XABAR BORADI
    bot.send_message(ADMIN_ID, order_text)


    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(
            f"Ism: {name}\n"
            f"Manzil: {address}\n"
            f"Telefon: {phone}\n"
            f"---\n"
        )

    bot.send_message(
        message.chat.id,
        "✅ Buyurtmangiz qabul qilindi!\n"
        "G‘ijduvon Toza Gilam xodimlari tez orada siz bilan bog‘lanadi 😊"
    )

print("Bot ishga tushdi...")

bot.polling()@bot.message_handler(func=lambda m: True)
def ai_operator(message):
    text = message.text.lower()

    if "narx" in text or "necha pul" in text:
        bot.send_message(
            message.chat.id,
            "💰 Narxlarimiz:\n"
            "1 m² = 10 000 so‘m\n\n"
            "O‘lchamni yozing, aniq hisoblab beraman 😊"
        )

    elif "qayer" in text or "manzil" in text:
        bot.send_message(
            message.chat.id,
            "📍 Biz G‘ijduvon tumanida ishlaymiz.\n"
            "Lokatsiya yuborsangiz, olib ketamiz 🚗"
        )

    elif "aloqa" in text or "telefon" in text:
        bot.send_message(
            message.chat.id,
            "📞 Aloqa:\n93 841 89 00\n90 614 26 73"
        )

    elif "qanday" in text:
        bot.send_message(
            message.chat.id,
            "🧼 Gilamlar avtomat usulda yuviladi,\n"
            "dezinfeksiya qilinadi va quritiladi.\n"
            "Sifat kafolatlanadi ✅"
        )

    else:
        bot.send_message(
            message.chat.id,
            "🤖 Men AI operator.\n"
            "Narx, aloqa yoki buyurtma haqida yozing 😊"
        )

