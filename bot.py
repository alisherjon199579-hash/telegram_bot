        import telebot
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8585152490:AAEUgPEFQIwRnHn9mLJyCy5JFTKuEpZUvgM"
bot = telebot.TeleBot(BOT_TOKEN)

FUE = {1000:3500000,2000:7000000,2500:8000000,3000:9500000,3500:11000000,
       4000:12000000,4500:13000000,5000:14000000}
PRP = 250000
MESO = 300000

users = {}

def s(x): return f"{x:,}".replace(",", ".")

def kb():
    k = InlineKeyboardMarkup()
    k.add(
        InlineKeyboardButton("➕ PRP", callback_data="prp"),
        InlineKeyboardButton("➕ Mezoterapiya", callback_data="meso")
    )
    k.add(InlineKeyboardButton("✅ Hisoblash", callback_data="done"))
    return k

@bot.message_handler(func=lambda m: True)
def base(message):
    t = message.text.lower()
    uid = message.from_user.id
    m = re.search(r'(\d+)\s*fue', t)
    if not m: return
    g = int(m.group(1))
    if g not in FUE:
        bot.reply_to(message,"❌ Bu graft yo‘q")
        return
    users[uid]={"base":FUE[g],"prp":0,"meso":0}
    bot.reply_to(message,f"💰 Asosiy: {s(FUE[g])} so‘m\nQo‘shimcha tanlang👇",reply_markup=kb())

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    u=c.from_user.id
    if u not in users: return
    if c.data=="prp": users[u]["prp"]=PRP
    if c.data=="meso": users[u]["meso"]=MESO
    if c.data=="done":
        t=users[u]["base"]+users[u]["prp"]+users[u]["meso"]
        bot.edit_message_text(f"🧾 JAMI: {s(t)} so‘m",c.message.chat.id,c.message.message_id)

bot.polling(none_stop=True)    
