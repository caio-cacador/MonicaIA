import telepot
from telepot.loop import MessageLoop
import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode

from constants import TAG_FILTER


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


def simplify(msg: str):
    return unidecode(msg.lower())


def get_answer_clean(theme: str, content: str):
    theme = simplify(theme)
    soup = BeautifulSoup(content, 'html.parser')
    paragraphs = soup.findAll(name='p')
    complete_answer = []
    for p in paragraphs:
        phrase = re.sub("\"|”|“|(\s\s)", '', str(p)).lower()
        phrase = re.sub(TAG_FILTER, '', phrase)
        if 'http' not in phrase:
            if theme in phrase and 'é' in phrase:

                complete_answer.append(phrase.replace('.,', '.').replace(': ;', ';'))
                # fim
                if re.findall("\.$", phrase):
                    _str = ''
                    for answer in complete_answer:
                        _str += answer
                    return _str
