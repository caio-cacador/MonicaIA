# !/usr/bin/env python

import telepot
from telepot.loop import MessageLoop
from constants import LINK_FILTER, MONICA_FILTER, TAG_FILTER, TOKEN, URL_SEARCH, WHAT_IS_INTERPRETER, WHO_IS_INTERPRETER
from monica import Monica


def send_msg_to(msg, chat_id):
    try:
        bot.sendMessage(chat_id, msg)
    except telepot.exception.TelegramError:
        print("[-] Chat not found... '", chat_id, "'")


def handle(msg):
    try:
        print("[-] (", msg['chat']['id'], ') ' + str(msg['from']['first_name']) + " sent: " + str(msg['text']))
        message = str(msg['text'])
        if message[0:6].lower() in MONICA_FILTER:
            message = message[7::].strip()
            if message:
                chat_id = msg['chat']['id']
                monica.message_interpreter(message=message, chat_id=chat_id)
    except Exception as ex:
        print('[-] Erros >> ', ex)


bot = telepot.Bot(TOKEN)
monica = Monica(bot)
MessageLoop(bot, handle).run_as_thread()
while True:
    pass