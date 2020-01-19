import telepot
from telepot.loop import MessageLoop
import requests
from bs4 import BeautifulSoup
import re
from google import google

from constants import LINK_FILTER, MONICA_FILTER, TAG_FILTER, TOKEN, URL_SEARCH, WHO_IS_INTERPRETER, WHAT_IS_INTERPRETER


class Utils:

    @staticmethod
    def request(url: str):
        try:
            request = requests.get(url, timeout=3)
            if request.status_code == 200:
                content = request.content
                return content
        except Exception as ex:
            pass

    # def get_links_from_question(self, content):
    #     soup = BeautifulSoup(content, 'html.parser')
    #     list_h2 = soup.findAll('h2')
    #     link_list = []
    #     for link in re.findall("href=\".*?\"", str(list_h2)):
    #         if link not in LINK_FILTER:
    #             link_list.append(link.replace('href=', '').replace('"', ''))
    #     return link_list

    @staticmethod
    def get_answer_clean(theme: str, content: str):
        soup = BeautifulSoup(content, 'html.parser')
        paragraphs = soup.findAll(name='p')
        complete_answer = []
        for p in paragraphs:
            phrase = str(p)
            if 'http' not in phrase:
                if theme in phrase and 'é' in phrase:
                    string = re.sub(TAG_FILTER, '', str(p))
                    complete_answer.append(string.replace('.,', '.').replace(': ;', ';'))
                    # fim
                    if re.findall("\.$", str(string)):
                        return complete_answer[0]
