import telebot
from telebot import types

TOKEN = "8252134065:AAEAHlbftOBZ-z7iWmqbknOo9QQAUC4ijRo"
ADMIN_ID = 282155346  # o'zingni telegram ID

bot = telebot.TeleBot(TOKEN)

# 🔘 START MENU
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("🛒 Buyurtma berish")
    btn2 = types.KeyboardButton("📏 Gilam m² hisoblash")
    btn3 = types.KeyboardButton("📞 Telefon yuborish", request_contact=True)
    btn4 = types.KeyboardButton("📍 Lokatsiya yuborish", request_location=True)
    btn5 = types.KeyboardButton("👨‍💼 Operator")
    btn6 = types.KeyboardButton("ℹ️ Xizmatlar")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)

    bot.send_message(message.chat.id, "Kerakli bo‘limni tanlang:", reply_markup=markup)

# 🧠 MENU BOSHQARUV
@bot.message_handler(func=lambda message: True)
def menu(message):

    if message.text == "🛒 Buyurtma berish":
        bot.send_message(message.chat.id, "Ismingizni yozing:")
        bot.register_next_step_handler(message, get_name)

    elif message.text == "📏 Gilam m² hisoblash":
        bot.send_message(message.chat.id, "Uzunlikni yozing (metr):")
        bot.register_next_step_handler(message, get_length)

    elif message.text == "👨‍💼 Operator":
        bot.send_message(message.chat.id, "Operatorga yozing:")
        bot.register_next_step_handler(message, send_to_admin)

    elif message.text == "ℹ️ Xizmatlar":
        bot.send_message(message.chat.id, "🧼 Biz gilam yuvish xizmatini tez va sifatli bajaramiz 🚀")

# 🛒 BUYURTMA QISMI
def get_name(message):
    name = message.text
    bot.send_message(message.chat.id, "Manzilingizni yozing:")
    bot.register_next_step_handler(message, get_address, name)

def get_address(message, name):
    address = message.text
    bot.send_message(message.chat.id, "Telefon raqamingizni yozing:")
    bot.register_next_step_handler(message, save_order, name, address)

def save_order(message, name, address):
    phone = message.text

    order_text = f"""
📥 YANGI BUYURTMA!

👤 Ism: {name}
🏠 Manzil: {address}
📞 Telefon: {phone}
"""

    # 📁 Faylga yozish
    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(order_text + "\n-----------------\n")

    # 👤 Mijozga javob
    bot.send_message(
        message.chat.id,
        "✅ Buyurtmangiz qabul qilindi!\n📞 Tez orada siz bilan bog‘lanamiz 😊"
    )

    # 👨‍💼 Adminga yuborish
    bot.send_message(ADMIN_ID, order_text)

# 📏 HISOBLASH
def get_length(message):
    try:
        length = float(message.text)
        bot.send_message(message.chat.id, "Enini yozing (metr):")
        bot.register_next_step_handler(message, get_width, length)
    except:
        bot.send_message(message.chat.id, "❌ Raqam kiriting")

def get_width(message, length):
    try:
        width = float(message.text)
        area = length * width
        bot.send_message(message.chat.id, f"📏 Maydon: {area} m²")
    except:
        bot.send_message(message.chat.id, "❌ Raqam kiriting")

# 👨‍💼 OPERATOR
def send_to_admin(message):
    bot.send_message(ADMIN_ID, f"📩 Mijozdan:\n{message.text}")
    bot.send_message(message.chat.id, "Xabaringiz yuborildi ✅")

# 📞 TELEFON QABUL QILISH
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    phone = message.contact.phone_number
    bot.send_message(message.chat.id, f"📞 Raqamingiz qabul qilindi: {phone}")
    bot.send_message(ADMIN_ID, f"📞 Yangi telefon: {phone}")

# 📍 LOKATSIYA QABUL QILISH
@bot.message_handler(content_types=['location'])
def location_handler(message):
    lat = message.location.latitude
    lon = message.location.longitude
    bot.send_message(message.chat.id, "📍 Lokatsiya qabul qilindi!")
    bot.send_message(ADMIN_ID, f"📍 Lokatsiya:\n{lat}, {lon}")

print("Bot ishga tushdi...")
bot.polling()
