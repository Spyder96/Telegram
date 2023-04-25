import telegram
from dotenv import load_dotenv
import os
import YFinance as YF

load_dotenv()
TelegramBotCredential = os.environ.get('BOT_TOKEN')

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def start(update, context):
    update.message.reply_text("Hi! I'm a bot. How can I help you?")


def handle_message(update, context):
    text = str(update.message.text).lower()


def search(update, context):
    ticker = context.args[0]

    stock = YF.Stock(ticker)
    update.message.reply_text(f" Getting Stock Details of :  {ticker} . Please wait... ")
    stock.get_data()
    if stock.data is None:
        update.message.reply_text(f" Failed to get Data for {ticker} ")
        logging.info(f"Failed to get stock data ")
    else:
        update.message.reply_text(f"last details : \n{stock.show_data()} ")
    # except Exception as e:
    #    logging.info(f"Failed to get stock data: {e} ")


#


# dispatcher.add_handler(MessageHandler( Filters.text, handle_message ))
#  with open('plot.png', 'rb') as f:
#     context.bot.send_photo(chat_id=update.effective_chat.id, photo=f)


def main():
    updater = Updater(TelegramBotCredential)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search", search))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
