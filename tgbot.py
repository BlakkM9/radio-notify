from telegram.ext import Updater, CommandHandler

updater = Updater(token="859620597:AAFk0xmDyAqwHokNndpyDkvSF1OGLA_S3O8")
# dispatcher = updater.dispatcher

chat_id = 43178708

# def start(bot, update):
#     global chat_id
#     global tg_bot
#     chat_id = update.message.chat_id
#     tg_bot = bot
#     send_message("chat_id: " + str(chat_id))
#     updater.stop()

def send_message(found_words_combined):

    updater.bot.send_message(chat_id, text)
    updater.bot.send_audio(chat_id, open("./rec/current.mp3", "rb"))

# start_handler = CommandHandler("start", start)
# dispatcher.add_handler(start_handler)
# updater.start_polling()
# updater.idle()
