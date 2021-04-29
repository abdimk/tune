import logging
from youtubesearchpython import SearchVideos
import json
from youtubesearchpython import SearchVideos
import time
import os
from telegram import InlineKeyboardMarkup,Update,ParseMode,InlineKeyboardButton,ChatAction
from telegram.ext import Updater, CallbackQueryHandler, MessageHandler, Filters
from telegram.ext import CallbackContext,CommandHandler
from telegram.error import BadRequest
#from youtube_search import YoutubeSearch

PORT = int(os.environ.get('PORT', 5000))

#from vid_utils import Video, BadLink
from vid_utils import Video, BadLink
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_format(update, context):
    logger.info("from {}: {}".format(update.message.chat_id, update.message.text)) # "history"
    keyboard = [
        [
            #InlineKeyboardButton("perivious", callback_data='1'),
            InlineKeyboardButton("Updates 🧩", url='https://t.me/Tuneln'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    pm = update.message.text
    first_name = update.message.chat.first_name
    if pm.lower() == "/start":
        update.message.reply_text(f'Hello <b>{first_name}</b> \n{context.bot.first_name} is a bot that helps you to download YouTube videos. It has a built-in YouTube <b>converter</b> to convert video to mp3, mp4, webm and web audio. This tool supports multiple audio and video formats. use <code>@vid</code> to search on YouTube',parse_mode=ParseMode.HTML,reply_markup=reply_markup)
    else:
        try:
            video = Video(update.message.text, init_keyboard=True)
        except BadLink:
            update.message.reply_text("Please send me the link from @vid")
        else:
            msg = str(update.message.text)
            search = SearchVideos(msg, offset = 1, mode = "json", max_results = 1)
            test = search.result()
            p = json.loads(test)
            q = p.get('search_result')
            msg = str(update.message.text)
            search = SearchVideos(msg, offset = 1, mode = "json", max_results = 1)
            test = search.result()
            p = json.loads(test)
            q = p.get('search_result')
            global t1
            t1 = q[0]['title']
            global d1
            d1 = q[0]['duration']
            global v1
            v1 = q[0]['views']
            thumbnails = q[0]['thumbnails'][-1]
            try:
                update.message.reply_photo(thumbnails)
            except BadRequest:
                 pass
            reply_markup = InlineKeyboardMarkup(video.keyboard)
            update.message.reply_text(f'Available *formats*:[image]({thumbnails})',reply_markup=reply_markup,parse_mode=ParseMode.MARKDOWN)

def download_choosen_format(update,CallbackContext):

    query = update.callback_query
    if query =='3' or query =='1' or query =='2':
        pass
    else:
        resolution_code, link = query.data.split(' ', 1)
        b1 =  b = updater.bot.edit_message_text(text="Making *Http* request...",chat_id=query.message.chat_id,message_id=query.message.message_id,parse_mode=ParseMode.MARKDOWN)
        time.sleep(2)
        b = updater.bot.edit_message_text(text="```Downloading...```",chat_id=query.message.chat_id,message_id=query.message.message_id,parse_mode=ParseMode.MARKDOWN)
        time.sleep(2)
        updater.bot.send_chat_action(chat_id=query.message.chat_id,action=ChatAction.UPLOAD_DOCUMENT)
        a = updater.bot.edit_message_text(text="```Uploading...```",chat_id=query.message.chat_id,message_id=query.message.message_id,parse_mode=ParseMode.MARKDOWN)


        video = Video(link)
        video.download(resolution_code)

        with video.send() as files:
            for f in files:
                updater.bot.send_document(chat_id=query.message.chat_id,document=open(f, 'rb'),caption=f'<b>Title</b>: {t1}\n<b>Duration</b>:<code>{d1}</code>\n<b>Views</b>:<code>{v1}</code>',parse_mode=ParseMode.HTML)

        time.sleep(2)
        a.delete()
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
TOKEN = "1717492682:AAF8R2JgoBX9KSG1WxlQcePQFZ7XgpnvcfM"
updater = Updater(TOKEN)

updater.dispatcher.add_handler(MessageHandler(Filters.text, get_format))
updater.dispatcher.add_error_handler(error)
updater.dispatcher.add_handler(CallbackQueryHandler(download_choosen_format))
#updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
#updater.bot.setWebhook('https://ridddel.herokuapp.com/' + TOKEN)
updater.start_polling()
updater.idle()
