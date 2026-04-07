import telebot
from telebot import types

TOKEN = "8252134065:AAEAHlbftOBZ-z7iWmqbknOo9QQAUC4ijRo"
ADMIN_ID =  282155346 

bot = telebot.TeleBot(TOKEN)

# 📦 saqlashlar
user_data = {}
users = set()

# 🔘 START
@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.chat.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 Buyurtma berish", "📏 Gilam m² hisoblash")
    markup.add("📞 Telefon yuborish", "📍 Lokatsiya yuborish")
    markup.add("👨‍💼 Operator", "ℹ️ Xizmatlar")

    bot.send_message(message.chat.id, "👋 Xush kelibsiz!", reply_markup=markup)

# 🧠 MENU
@bot.message_handler(func=lambda message: True)
def menu(message):

    if message.text == "🛒 Buyurtma berish":
        bot.send_message(message.chat.id, "Ismingizni yozing:")
        bot.register_next_step_handler(message, get_name)

    elif message.text == "📏 Gilam m² hisoblash":
        bot.send_message(message.chat.id, "Uzunlikni yozing:")
        bot.register_next_step_handler(message, get_length)

    elif message.text == "👨‍💼 Operator":
        bot.send_message(message.chat.id, "Operatorga yozing:")
        bot.register_next_step_handler(message, send_to_admin)

    elif message.text == "ℹ️ Xizmatlar":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🧼 Gilam", "🛏 Ko‘rpacha")
        markup.add("🛌 Adyol", "🪶 Yostiq")
        markup.add("⬅️ Orqaga")

        bot.send_message(message.chat.id, "Xizmatni tanlang:", reply_markup=markup)

    elif message.text == "🧼 Gilam":
        bot.send_message(message.chat.id, "Uzunligini yozing:")
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
    bot.send_message(message.chat.id, "Manzil yozing:")
    bot.register_next_step_handler(message, get_address, name)

def get_address(message, name):
    address = message.text
    bot.send_message(message.chat.id, "Telefon yozing:")
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
👤 {name}
🏠 {address}
📞 {phone}
"""

    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(order_text + "\n------\n")

    bot.send_message(message.chat.id, "✅ Qabul qilindi")
    bot.send_message(ADMIN_ID, order_text)

# 📏 HISOB
def get_length(message):
    try:
        length = float(message.text)
        bot.send_message(message.chat.id, "Enini yozing:")
        bot.register_next_step_handler(message, get_width, length)
    except:
        bot.send_message(message.chat.id, "❌ Raqam yoz")

def get_width(message, length):
    try:
        width = float(message.text)
        area = length * width
        price = area * 15000

        bot.send_message(message.chat.id, f"{area} m²\n{price} so‘m")
    except:
        bot.send_message(message.chat.id, "❌ Raqam yoz")

# 🧼 GILAM
def gilam_length(message):
    try:
        length = float(message.text)
        bot.send_message(message.chat.id, "Enini yozing:")
        bot.register_next_step_handler(message, gilam_width, length)
    except:
        bot.send_message(message.chat.id, "❌ Raqam yoz")

def gilam_width(message, length):
    try:
        width = float(message.text)
        area = length * width
        price = area * 10000

        user_data[message.chat.id] = {"area": area, "price": price}

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🛒 Buyurtma berish")

        bot.send_message(message.chat.id,
                         f"{area} m²\n{price} so‘m",
                         reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "❌ Raqam yoz")

# 👨‍💼 OPERATOR
def send_to_admin(message):
    bot.send_message(ADMIN_ID, f"📩 {message.text}")
    bot.send_message(message.chat.id, "Yuborildi")

# 📞 CONTACT
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    bot.send_message(ADMIN_ID, f"📞 {message.contact.phone_number}")

# 📍 LOCATION
@bot.message_handler(content_types=['location'])
def location_handler(message):
    bot.send_message(ADMIN_ID, f"📍 {message.location.latitude}, {message.location.longitude}")

# 📊 ADMIN PANEL
@bot.message_handler(commands=['orders'])
def orders(message):
    if message.chat.id == ADMIN_ID:
        try:
            with open("orders.txt", "r", encoding="utf-8") as f:
                bot.send_message(message.chat.id, f.read())
        except:
            bot.send_message(message.chat.id, "Bo‘sh")

@bot.message_handler(commands=['stats'])
def stats(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"Mijozlar: {len(users)}")

@bot.message_handler(commands=['send'])
def send_all(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Xabar yozing:")
        bot.register_next_step_handler(message, broadcast)

def broadcast(message):
    for user in users:
        try:
            bot.send_message(user, message.text)
        except:
            pass

print("🚀 Ishladi")
bot.polling()
