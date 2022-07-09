import json
import os
import threading

from com.nosehad.python.hash_c import Hash
from com.nosehad.python.url_decrypter_c import UrlDEC
from com.nosehad.python.url_encrypter_c import UrlENC


def confirm(uname):
    return uname not in os.listdir(os.getcwd() + '\\users')


def valid(email, passwd):
    if email not in os.listdir(os.getcwd() + '\\users') \
            or Hash(target_string=passwd, lenght=128, seed=email).get_hash() != User(email, -1).get_passwd():
        return False
    return True


def create(email, passwd):
    curdir = os.getcwd().split('\\')
    file = open(os.getcwd() + f'\\users\\{email}', "a")
    file.write(f"""
{{
  "passwd":"{Hash(target_string=passwd, lenght=128, seed=email).get_hash()}",
  "history":
  [
    "https://search.brave.com/"
  ],
  "settings": 
  {{
    "news":"true",
    "loading":"lazy"
  }}
}}
        """)
    file.close()


class User:
    def __init__(self, email=str(), session_id=-1, nocon=False):
        if nocon:
            return
        self.email = email
        self.encrypter = UrlENC(session_id)
        self.decrypter = UrlDEC(session_id)
        self.cookies = []

        def do():
            data: json = json.loads(
                open(os.getcwd() + f'\\users\\{self.email}', 'r').read())
            history = []
            i: int = 0
            for site in data['history']:
                i += 1
                history.append(site)
                if i == 100:
                    data['history'] = history
                    os.remove(os.getcwd() + f'\\users\\{self.email}')
                    file = open(os.getcwd() + f'\\users\\{self.email}', "a")
                    file.write(json.dumps(data))
                    file.close()

        threading.Thread(target=do).start()

    def get_decrypter(self):
        return self.decrypter

    def get_encrypter(self):
        return self.encrypter

    def add_to_history(self, item):
        data: json = json.loads(
            open(os.getcwd() + f'\\users\\{self.email}', 'r').read())
        history = [item]
        for site in data['history']:
            history.append(site)

        data['history'] = history
        os.remove(os.getcwd() + f'\\users\\{self.email}')
        file = open(os.getcwd() + f'\\users\\{self.email}', "a")
        file.write(json.dumps(data))
        file.close()

    def get_latest(self):
        data: json = json.loads(
            open(os.getcwd() + f'\\users\\{self.email}', 'r').read())
        return data['history'][0]

    def get_cookies(self, url):
        res = list()
        for cookie in self.cookies:
            if cookie[0] == url:
                res.append(cookie[1])
        return res

    def set_cookie(self, url, _cookie):
        _add = [url, _cookie]
        for cookie in self.cookies:
            if cookie == _add:
                return
            elif cookie[1][0] == _cookie[0]:
                cookie[1][1] = _cookie[1]
                return
        self.cookies.append(_add)

    def rem_cookie(self, url, cookie):
        for _cookie in self.cookies:
            if _cookie[0] == url and _cookie[1][0].startswith(cookie):
                self.cookies.remove(_cookie)
                return

    def get_history(self):
        res = []
        data: json = json.loads(
            open(os.getcwd() + f'\\users\\{self.email}', 'r').read())
        i: int = 0
        for site in data['history']:
            i += 1
            res.append(site)
            if i == 100:
                return res
        return res

    def get_setting(self, key):
        data: json = json.loads(
            open(os.getcwd() + f'\\users\\{self.email}', 'r').read())
        return data['settings'][key]

    def get_passwd(self):
        data: json = json.loads(
            open(os.getcwd() + f'\\users\\{self.email}', 'r').read())
        return data['passwd']

    def set_setting(self, key, value):
        data: json = json.loads(
            open(os.getcwd() + f'\\users\\{self.email}', 'r').read())
        data['settings'][key] = value
        os.remove(os.getcwd() + f'\\users\\{self.email}')
        file = open(os.getcwd() + f'\\users\\{self.email}', "a")
        file.write(json.dumps(data))
        file.close()
