       import os
import re
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv("8585152490:AAEUgPEFQIwRnHn9mLJyCy5JFTKuEpZUvgM")  # Railway Variables’dan olinadi
bot = telebot.TeleBot(BOT_TOKEN)

# Narxlar
FUE = {
    1000: 3500000,
    2000: 7000000,
    2500: 8000000,
    3000: 9500000,
    3500: 11000000,
    4000: 12000000,
    4500: 13000000,
    5000: 14000000
}

PRP = 250000
MESO = 300000

users = {}

def fmt(x):
    return f"{x:,}".replace(",", ".")

def keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("➕ PRP", callback_data="prp"),
        InlineKeyboardButton("➕ Mezoterapiya", callback_data="meso")
    )
    kb.add(InlineKeyboardButton("✅ Hisoblash", callback_data="done"))
    return kb

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text.lower()
    uid = message.from_user.id

    m = re.search(r'(\d+)\s*fue', text)
    if not m:
        return

    graft = int(m.group(1))
    if graft not in FUE:
        bot.reply_to(message, "❌ Bu graft uchun narx yo‘q")
        return

    users[uid] = {"base": FUE[graft], "prp": 0, "meso": 0}

    bot.reply_to(
        message,
        f"💉 FUE | 🧬 {graft} graft\n"
        f"💰 Asosiy narx: {fmt(FUE[graft])} so‘m\n\n"
        f"Qo‘shimcha xizmat tanlang 👇",
        reply_markup=keyboard()
    )

@bot.callback_query_handler(func=lambda c: True)
def callbacks(c):
    uid = c.from_user.id
    if uid not in users:
        return

    if c.data == "prp":
        users[uid]["prp"] = PRP
        bot.answer_callback_query(c.id, "PRP qo‘shildi")

    elif c.data == "meso":
        users[uid]["meso"] = MESO
        bot.answer_callback_query(c.id, "Mezoterapiya qo‘shildi")

    elif c.data == "done":
        total = users[uid]["base"] + users[uid]["prp"] + users[uid]["meso"]
        bot.edit_message_text(
            f"🧾 JAMI SUMMA:\n💳 {fmt(total)} so‘m",
            chat_id=c.message.chat.id,
            message_id=c.message.message_id
        )

bot.polling(none_stop=True) 
