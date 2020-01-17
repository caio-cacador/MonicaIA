# ----------------- DEPENDENCIES
# !/usr/bin/env python

import telepot
from telepot.loop import MessageLoop
import requests
from bs4 import BeautifulSoup
import re
from google import google


# ----------------- CONSTANTS
TOKEN = "891967726:AAF4iR0AknoObf_L-rwKIwjIxzeGtYdeTM4"

URL_SEARCH = 'https://www.ecosia.org/search?q=o+que+é+BUSCAR'

QUESTION_INTERPRETER = ('o que eh', 'o q eh', 'oq é', 'oque é', '?', 'o q é', 'oq é', 'o que é')

MONICA_FILTER = ('Monica', 'monica', 'MONICA', 'Mônica', 'mônica', 'MÔNICA')

LINK_FILTER = ('www.buscape', 'www.fastshop', 'www.zoom', 'www.magazineluiza', 'www.xvideos', 'www.porhub')

TAG_FILTER = "<img.?>|<p class=\".?\">|<a href.?\">|href.?\">|<.?>|</strong>|<strong>|<a class=.?>|" + \
             "<span>\[.?\]</span>|<sup.?>|<p>|<b>|</b>|<br>|</br>|<br/>|<a>|</a>|</sup>|</p>|<i>|" + \
             "</i>|</sub>|<sub>|<span.?span></span>|<span.?</span>|<small>|</small>|\\xa0|<\/span>\)<\/span>|" + \
             "<\/span>\(<\/span>"


class MonicaBusca:
    # chat_id = -1001318092698

    def _request(self, url):
        try:
            request = requests.get(url, timeout=3)
            if request.status_code == 200:
                content = request.content
                return content
        except Exception as ex:
            pass

    def get_links_from_question(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        list_h2 = soup.findAll('h2')
        link_list = []
        for link in re.findall("href=\".*?\"", str(list_h2)):
            if link not in LINK_FILTER:
                link_list.append(link.replace('href=', '').replace('"', ''))
        return link_list

    def get_answer_clean(self, theme, content):
        soup = BeautifulSoup(content, 'html.parser')
        paragraphs = soup.findAll(name='p')
        complete_answer = []
        for p in paragraphs:
            if theme in str(p) and 'é' in str(p):
                string = re.sub(TAG_FILTER, '', str(p))
                complete_answer.append(string.replace('.,', '.').replace(': ;', ';'))
                # fim
                if re.findall("\.$", str(string)):
                    return complete_answer[0]

    def question_interpretor(self, question):
        theme = ''
        for item in QUESTION_INTERPRETER:
            if item in question:
                theme = question.replace(item, '')
                # question = "o+que+é+" + theme.strip().replace(' ', '+')
                break
        return theme.strip()

    def buscar(self, question):
        theme = self.question_interpretor(question)
        try:
            search = 'o que é ' + theme
            print('search: ', search)
            links = (res.link if res.link not in LINK_FILTER else '' for res in google.search(search))
            print(f'links: {links}')
            for link in links:
                answer = self._request(link)
                if answer:
                    clear_answer = self.get_answer_clean(theme, answer)
                    if clear_answer:
                        return str(clear_answer)

            return "Por favor, tente especificar a sua pergunta..."

        except KeyboardInterrupt:
            pass
        except Exception as ex:
            print('Error >>>', ex)


def send_msg_to(msg, chat_id):
    try:
        bot.sendMessage(chat_id, msg)
    except telepot.exception.TelegramError:
        print("[-] Chat not found... '", chat_id, "'")


def handle(msg):
    try:
        #       print("[+] In chat: " + str(msg['chat']['id']))
        print("[-] (", msg['chat']['id'], ') ' + str(msg['from']['first_name']) + " sent: " + str(msg['text']))
        message = str(msg['text'])
        # last_chat_id = msg['chat']['id']
        if message.split(' ' or ',')[0].strip(',').strip(' ') in MONICA_FILTER:
            message = message.split(',' or ' ', 1)[1]
            if message:
                chat_id = msg['chat']['id']
                send_msg_to('Deixe me ver...', chat_id)
                response = monicaBusca.buscar(message)
                send_msg_to(response, chat_id)
    except Exception:
        pass


bot = telepot.Bot(TOKEN)

last_chat_id = ''
monicaBusca = MonicaBusca()

MessageLoop(bot, handle).run_as_thread()

while True:
    pass
    # try:
    #     #         -1001318092698
    #     chatId_msg = input("\n>> chat id and message\n>> ").split(' ', 1)
    #     chat_id = chatId_msg[1]
    #     if 'id-' not in chat_id:
    #         chat_id = last_chat_id
    #     send_msg_to(chat_id, chatId_msg[0])
    #     pass
    # except KeyboardInterrupt:
    #     bot.stopMessageLiveLocation
    # except Exception:
    #     pass