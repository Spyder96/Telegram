import telegram
from dotenv import load_dotenv
import os
import YFinance as YF
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import pyautogui

CHAT_ID = 727464642
load_dotenv()
TelegramBotCredential = os.environ.get('BOT_TOKEN')

# Define states for the conversation handler
START, WAITING_INPUT = range(2)

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


def start(update, context):
    update.message.reply_text("Hi! I'm a bot. How can I help you?")


def handle_message(update, context):
    text = str(update.message.text).lower()

def screenshot(update, context):
            current_x, current_y = pyautogui.position()

# Move the mouse by one pixel
            pyautogui.move(1, 1)

# Alternatively, you can move the mouse relative to its current position
# pyautogui.moveRel(1, 1)

# Optionally, you can return the mouse to its original position
            pyautogui.moveTo(current_x, current_y)
            screenshot = pyautogui.screenshot()
            # Save the screenshot as a file
            screenshot.save('screenshot.png')
            context.bot.send_photo(chat_id=CHAT_ID, photo=open('screenshot.png', 'rb'), caption= "SS")

def search_t(update, context):
    ticker = context.args[0]

    stock = YF.Stock(ticker)
    update.message.reply_text(f" Getting Stock Details of :  {ticker} \n Please wait... ")
    stock.get_data()
    if stock.data is None:
        update.message.reply_text(f" Failed to get Data for {ticker} ")
        logging.info(f"Failed to get stock data ")
    else:
        update.message.reply_text(f"last details : \n{stock.show_data()} ")
    # except Exception as e:
    #    logging.info(f"Failed to get stock data: {e} ")
    

    while True:
        update.message.reply_text("Waiting for user input. Send 'exit' to stop.")
        user_input = update.message.text.lower()

        if user_input == 'exit':
            break

        if user_input == 'trend':
            stock.set_period_values()
            stock.trendline()
            stock.plot_trends()
            with open('plot.png', 'rb') as f:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=f)


def search_start(update, context):
    ticker = context.args[0]
    context.chat_data['ticker'] = ticker 
    update.message.reply_text("Enter the ticker symbol to get stock details:")
    return WAITING_INPUT


def handle_user_input(update, context):
    user_input = update.message.text.lower()

    if user_input == 'exit':
        update.message.reply_text("Exiting the search.")
        return ConversationHandler.END

    if user_input == 'trend':
        # Perform trend-related actions here
        ticker = context.chat_data.get('ticker')  # Retrieve the ticker from chat_data
        update.message.reply_text(f"getting Data for {ticker}")

        if ticker:
            stock = YF.Stock(ticker)
            stock.get_data()

            if stock.data is None:
                update.message.reply_text(f"Failed to get Data for {ticker}")
                logging.info("Failed to get stock data")
            else:
                stock.set_period_values()
                stock.trendline()
                stock.plot_trends()
                with open('plot.png', 'rb') as f:
                    context.bot.send_photo(chat_id=update.effective_chat.id, photo=f)
        else:
            update.message.reply_text(f"Failed to get ticker. Please search again")

    # Return to waiting for input state
    update.message.reply_text("Waiting for user input. Send 'exit' to stop.")
    return WAITING_INPUT


#


# dispatcher.add_handler(MessageHandler( Filters.text, handle_message ))



def main():
    updater = Updater(TelegramBotCredential)
    dispatcher = updater.dispatcher

    # # Creating a conversation handler
    # conv_handler = telegram.ext.ConversationHandler(
    #     entry_points=[CommandHandler("search", search)],
    #     states={
    #         WAITING_INPUT: [MessageHandler(Filters.text, handle_user_input)]
    #     },
    #     fallbacks=[CommandHandler("exit", exit)]
    # )
        # Creating a conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("search", search_start)],
        states={
            WAITING_INPUT: [MessageHandler(Filters.text, handle_user_input)]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("screenshot", screenshot))
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
