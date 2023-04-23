
import telegram
from dotenv import load_dotenv
import os

load_dotenv()
TelegramBotCredential = os.environ.get('BOT_TOKEN')

import logging
from telegram.ext import Updater, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update, context):
    update.message.reply_text ("Hi! I'm a bot. How can I help you?")
    
def search(update, context):
    update.message.reply_text ("Enter text to search?")
    ticker = context.args[0]
    
    
def main():
    updater = Updater(TelegramBotCredential)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search", search))
    
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()