import telebot
from telebot import types

TOKEN = "8252134065:AAEAHlbftOBZ-z7iWmqbknOo9QQAUC4ijRo"
ADMIN_ID = 282155346

bot = telebot.TeleBot(TOKEN)

# 📦 vaqtincha saqlash (hisob natijasi)
user_data = {}

# 🔘 START
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("🛒 Buyurtma berish", "📏 Gilam m² hisoblash")
    markup.add("📞 Telefon yuborish", "📍 Lokatsiya yuborish")
    markup.add("👨‍💼 Operator", "ℹ️ Xizmatlar")

    bot.send_message(message.chat.id, "👋 Xush kelibsiz!\nKerakli bo‘limni tanlang:", reply_markup=markup)

# 🧠 MENU
@bot.message_handler(func=lambda message: True)
def menu(message):

    if message.text == "🛒 Buyurtma berish":
        bot.send_message(message.chat.id, "Ismingizni yozing:")
        bot.register_next_step_handler(message, get_name)

    elif message.text == "📏 Gilam m² hisoblash":
        bot.send_message(message.chat.id, "Uzunlikni yozing (metr):")
        bot.register_next_step_handler(message, get_length)

    elif message.text == "👨‍💼 Operator":
        bot.send_message(message.chat.id, "✍️ Operatorga yozing:")
        bot.register_next_step_handler(message, send_to_admin)

    elif message.text == "ℹ️ Xizmatlar":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🧼 Gilam", "🛏 Ko‘rpacha")
        markup.add("🛌 Adyol", "🪶 Yostiq")
        markup.add("⬅️ Orqaga")

        bot.send_message(message.chat.id, "Xizmatni tanlang:", reply_markup=markup)

    elif message.text == "🧼 Gilam":
        bot.send_message(message.chat.id, "Uzunligini yozing (metr):")
        bot.register_next_step_handler(message, gilam_length)

    elif message.text == "🛏 Ko‘rpacha":
        bot.send_message(message.chat.id, "💰 30 000 – 60 000 so‘m")

    elif message.text == "🛌 Adyol":
        bot.send_message(message.chat.id, "💰 60 000 so‘m")

    elif message.text == "🪶 Yostiq":
        bot.send_message(message.chat.id, "💰 25 000 so‘m")

    elif message.text == "⬅️ Orqaga":
        start(message)

# 🛒 BUYURTMA
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

    extra = ""
    if message.chat.id in user_data:
        data = user_data[message.chat.id]
        extra = f"\n🧼 Gilam: {data['area']} m²\n💰 Narx: {data['price']} so‘m\n"

    order_text = f"""
📥 YANGI BUYURTMA!
{extra}
👤 Ism: {name}
🏠 Manzil: {address}
📞 Telefon: {phone}
"""

    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(order_text + "\n-----------\n")

    bot.send_message(message.chat.id, "✅ Buyurtma qabul qilindi!")

    bot.send_message(ADMIN_ID, order_text)

# 📏 HISOB (umumiy)
def get_length(message):
    try:
        length = float(message.text)
        bot.send_message(message.chat.id, "Enini yozing:")
        bot.register_next_step_handler(message, get_width, length)
    except:
        bot.send_message(message.chat.id, "❌ Raqam kiriting")

def get_width(message, length):
    try:
        width = float(message.text)
        area = length * width
        price = area * 10000

        bot.send_message(message.chat.id, f"📏 {area} m²\n💰 Narxi: {price} so‘m")
    except:
        bot.send_message(message.chat.id, "❌ Raqam kiriting")

# 🧼 GILAM MAXSUS HISOB
def gilam_length(message):
    try:
        length = float(message.text)
        bot.send_message(message.chat.id, "Enini yozing (metr):")
        bot.register_next_step_handler(message, gilam_width, length)
    except:
        bot.send_message(message.chat.id, "❌ Raqam yozing")

def gilam_width(message, length):
    try:
        width = float(message.text)
        area = length * width
        price = area * 10000

        user_data[message.chat.id] = {
            "area": area,
            "price": price
        }

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🛒 Buyurtma berish")

        bot.send_message(
            message.chat.id,
            f"📏 Maydon: {area} m²\n💰 Narxi: {price} so‘m",
            reply_markup=markup
        )

    except:
        bot.send_message(message.chat.id, "❌ Raqam yozing")

# 👨‍💼 OPERATOR
def send_to_admin(message):
    bot.send_message(ADMIN_ID, f"📩 Mijoz:\n{message.text}")
    bot.send_message(message.chat.id, "✅ Operatorga yuborildi")

# 📞 TELEFON
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    phone = message.contact.phone_number
    bot.send_message(ADMIN_ID, f"📞 Telefon: {phone}")
    bot.send_message(message.chat.id, "✅ Raqam olindi")

# 📍 LOKATSIYA
@bot.message_handler(content_types=['location'])
def location_handler(message):
    lat = message.location.latitude
    lon = message.location.longitude
    bot.send_message(ADMIN_ID, f"📍 Lokatsiya:\n{lat}, {lon}")
    bot.send_message(message.chat.id, "✅ Lokatsiya olindi")

print("🚀 Bot ishga tushdi...")
bot.polling()
