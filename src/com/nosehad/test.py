import random
import time

import requests

from src.com.nosehad.python import url, logger
from src.com.nosehad.python.cookie import Cookie
from src.com.nosehad.python.logger import Logger
from src.com.nosehad.python.random_c import Random
from src.com.nosehad.python.replacer_c import ReplacerHtml
from src.com.nosehad.python.requester_c import Requester
from src.com.nosehad.python.session_server import Sessions
from src.com.nosehad.python.user_c import *

# print(url.filter_links(open('./assets/test.min.css', 'r').read(), 'https://iuri.is', UrlENC(-2)))


encrypter = UrlENC(-2)


# test=("/lol".().send(\'https://amazon.de\'))

def regex_text(string):
    temp = [False, 0, str(), str()]
    for integer in range(len(string)):
        # print(integer, integer+1)
        if (string[integer] + string[integer + 1]) == '<p' or \
                (string[integer] + string[integer + 1]) == '<h' or \
                (string[integer] + string[integer + 1]) == '<t':
            temp[2], temp[0], temp[1] = string[integer] + string[integer + 1], True, integer
        elif not temp[0]:
            temp[3] += string[integer]
        elif (string[integer] + string[integer + 1] + string[integer + 2]) == temp[2].replace('<', '</'):
            _temp = str()
            for number in range(temp[1], integer + 1, +1):
                _temp = string[number] if string[number] != '\'' and string[number] != '\"' else ''
            temp[0], temp[3] = False, temp[3] + _temp
    return temp[3]

