import telebot
import sqlite3

TOKEN = "8686862211:AAEQba68u6edewV-6nWkEzC5tw5b9xsNssI"
ADMIN_ID = 7397475374

bot = telebot.TeleBot(TOKEN)

def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS buyers(
        user_id INTEGER
    )
    """)
    conn.commit()
    conn.close()

init_db()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
    "Welcome!\n\nPress /buy to purchase.")

@bot.message_handler(commands=['buy'])
def buy(message):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("SELECT * FROM buyers WHERE user_id=?", (message.chat.id,))
    if c.fetchone():
        bot.send_message(message.chat.id, "You already bought.")
        return

    c.execute("INSERT INTO buyers (user_id) VALUES (?)", (message.chat.id,))
    conn.commit()

    c.execute("SELECT COUNT(*) FROM buyers")
    total = c.fetchone()[0]

    bot.send_message(message.chat.id, "Purchase recorded ✅")
    bot.send_message(ADMIN_ID, f"New buyer!\nTotal buyers: {total}")

bot.infinity_polling()
