import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import logging

# Bot Token (Render-এ আপলোড করার আগে Environment Variable এ সেট করতে হবে)
TOKEN = "8433316238:AAHNJxtRwwOt2c0LD6U_-O7-xWI9F4mpjyM"
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start command
def start(update, context):
    update.message.reply_text("✅ Bot is online! Send me any text and I will echo it.")

# Echo function
def echo(update, context):
    text = update.message.text
    update.message.reply_text(f"You said: {text}")

# Dispatcher setup
dispatcher = Dispatcher(bot, update_queue=None, workers=0, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Bot is running..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
