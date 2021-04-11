import logging
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,Update)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1711329030:AAERyXxw0UnzNTCLAf-EkT9UZ4cWvt01ayM'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            #InlineKeyboardButton("perivious", callback_data='1'),
            InlineKeyboardButton("🧩Server", callback_data='2'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    first_name = update.message.chat.first_name
    update.message.reply_text(f'''Hello <b>{first_name}</b> This {context.bot.first_name} bot it will help you to <b>download</b> musics with the best quality available as fast as possilbe. use @vid for inline''',parse_mode=ParseMode.HTML,reply_markup=reply_markup)
    global global_user
    global_user = str(first_name)
def button(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Back", callback_data='3'),
            #InlineKeyboardButton("", callback_data='4'),
            #InlineKeyboardButton("right", callback_data='2'),
        ],
        
    ]
    
    keyboard2 = [
        [
            #InlineKeyboardButton("perivious", callback_data='1'),
            InlineKeyboardButton("🧩Server", callback_data='1'),
        ],
        
    ]
    reply_markup2 = InlineKeyboardMarkup(keyboard2)
    query2 = update.callback_query
    if query2.data =='3':
        query2.answer()
        query2.edit_message_text(text=f'''Hello <b>{global_user}</b> This {context.bot.first_name} bot it will help you to <b>download</b> musics with the best quality available as fast as possilbe. use @vid for inline''',parse_mode=ParseMode.HTML,reply_markup=reply_markup2)
    else:
        reply_markup = InlineKeyboardMarkup(keyboard)
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=f"<b>version</b>: <code>1.2.1</code>\n<b>server</b>: <code>Delta</code>\n<b>status</b>: <code>online</code>\n<b>Developer</b> :@paperexted\n",parse_mode=ParseMode.HTML,reply_markup=reply_markup)
    

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://tune.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
