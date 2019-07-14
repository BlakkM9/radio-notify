from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
import atexit
import re

import utils
import data

message_ids = []

token = open("token.txt", "r").read()

updater = Updater(token=token)


# dispatcher = updater.dispatcher

# def start(bot, update):
#     global chat_id
#     global tg_bot
#     chat_id = update.message.chat_id
#     tg_bot = bot
#     send_message("chat_id: " + str(chat_id))
#     updater.stop()


def send_message(found_words, rec_text):
    # combine found words
    found_words_combined = utils.combine_string(found_words, ", ")
    print("[T] KEYWORDS FOUND: " + found_words_combined)

    # highlight words
    for w in found_words:
        rec_text = re.sub(r"\b({0})\b".format(w), "<code>" + w + "</code>", rec_text, flags=re.IGNORECASE)
        # rec_text = re.sub(r"\b({0})\b".format(w), "*" + w + "*", rec_text, flags=re.IGNORECASE)

    # # put in code tag NESTED TAGS NOT WORKING!
    # rec_text = "<pre>" + rec_text + "</pre>"
    # # rec_text = "_" + rec_text + "_"

    text = ("<b>Keywords detected on " + data.radio_name + ":</b>\n<code>" + found_words_combined + "</code>\n\n" +
            "<b>Original text:</b>\n" + rec_text)

    message_ids.append(updater.bot.send_message(data.chat_id, text, parse_mode=ParseMode.HTML).message_id)
    message_ids.append(updater.bot.send_voice(data.chat_id, open("./rec/current.ogg", "rb")))


# deletes all messages saved in messages
def clear_chat():
    print("deleting " + str(len(message_ids)) + " messages")
    for m in message_ids:
        updater.bot.delete_message(data.chat_id, m)


# TODO move to start script and use oop!!
# delete messages when exiting application
atexit.register(clear_chat)

# start_handler = CommandHandler("start", start)
# dispatcher.add_handler(start_handler)
# updater.start_polling()
# updater.idle()
