import random

import telepot
import utils
from google import google
import interpreters
from constants import LINK_FILTER, NORMAL_GREETING, INFORMAL_GREETING, GREETING_WITH_QUESTION, COMPLIMENT_RESPONSE


class Monica:
    def __init__(self, bot: telepot):
        self.bot = bot
    # chat_id = -1001318092698

    def message_interpreter(self, message: str, firt_name: str, chat_id):

        if firt_name == 'Adriano':
            self._response('Desculpe Adriano, não posso conversar com nóias por enquanto.', chat_id)

        if interpreters.is_what_is_question(message):
            self._response('Deixe me ver...', chat_id)
            self._response(self._what_is(message), chat_id)

        elif interpreters.is_who_is_question(message):
            self._response('Deixe me ver...', chat_id)
            self._response(self._who_is(message), chat_id)

        elif interpreters.is_it_a_conversation(message):
            response = self._talk(message).replace('vc', 'você')
            self._response(response, chat_id)

        elif interpreters.is_it_a_compliment(message):
            self._response(random.choice(COMPLIMENT_RESPONSE), chat_id)


    def _what_is(self, question):
        theme = interpreters.what_is_interpreter(question)
        try:
            search = 'o que é ' + theme
            print('[+] Searching: ', search)
            links = (res.link if res.link not in LINK_FILTER else '' for res in google.search(search))
            for link in links:
                content = utils.request(url=link)
                if content:
                    clear_answer = utils.get_answer_clean(theme=theme, content=content)
                    if clear_answer:
                        return clear_answer

            return "Por favor, tente especificar a sua pergunta..."

        except KeyboardInterrupt:
            pass
        except Exception as ex:
            print('Error >>>', ex)

    def _who_is(self, question):
        theme = interpreters.who_is_interpreter(question)
        try:
            search = 'quem é ' + theme
            print('[+] Searching: ', search)
            links = (res.link if res.link not in LINK_FILTER else '' for res in google.search(search))
            for link in links:
                content = utils.request(url=link)
                if content:
                    clear_answer = utils.get_answer_clean(theme=theme, content=content)
                    if clear_answer:
                        return clear_answer

            return "Por favor, tente especificar a sua pergunta..."

        except KeyboardInterrupt:
            pass
        except Exception as ex:
            print('Error >>>', ex)

    @staticmethod
    def _talk(phrase):
        for gretting in NORMAL_GREETING:
            if gretting in phrase:
                return random.choice(NORMAL_GREETING).capitalize()
        for gretting in INFORMAL_GREETING:
            if gretting in phrase:
                return random.choice(INFORMAL_GREETING).capitalize()
        for gretting in GREETING_WITH_QUESTION:
            if gretting in phrase:
                return 'Estou bem, e vc, ' + random.choice(GREETING_WITH_QUESTION) + '?'

    def _response(self, msg: str, chat_id):
        try:
            self.bot.sendMessage(chat_id, msg)
        except Exception as ex:
            print('[-] Error >> ', ex)


