# !/usr/bin/env python

import telepot
from telepot.loop import MessageLoop
from unidecode import unidecode
from constants import MONICA_FILTER, TOKEN
from monica import Monica


def send_msg_to(msg, chat_id):
    try:
        bot.sendMessage(chat_id, msg)
    except telepot.exception.TelegramError:
        print("[-] Chat not found... '", chat_id, "'")


def handle(msg):
    try:
        print("[-] (", msg['chat']['id'], ') ' + str(msg['from']['first_name']) + " sent: " + str(msg['text']))

        # remove a acentuação e converte para minusculo
        message = unidecode(str(msg['text']).lower())

        if message[0:6] in MONICA_FILTER:
            message = message[7::].strip()
            if message:
                chat_id = msg['chat']['id']
                firt_name = str(msg['from']['first_name'])
                monica.message_interpreter(message=message, chat_id=chat_id, firt_name=firt_name)
    except Exception as ex:
        print('[-] Erros >> ', ex)


bot = telepot.Bot(TOKEN)
monica = Monica(bot)
MessageLoop(bot, handle).run_as_thread()
bot.sendMessage(-1001318092698, 'Estou online clan!')
while True:
    pass