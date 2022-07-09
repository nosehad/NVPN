import os

import requests

from com.nosehad.python import url
from com.nosehad.python.map_c import Map
from com.nosehad.python.requester_c import Requester
from com.nosehad.python.url_decrypter_c import UrlDEC
from com.nosehad.python.user_c import User


class Server:
    def __init__(self):
        self.frame = open(os.getcwd() + "\\assets\\frame.html", 'r').read()
        self.welcome = open(os.getcwd() + "\\assets\\welcome.html", 'r').read()
        self.home = open(os.getcwd() + "\\assets\\home.html", 'r').read()
        self.noperm = open(os.getcwd() + "\\assets\\noperm.html", 'r').read()
        self.login = open(os.getcwd() + "\\assets\\login.html", 'r').read()
        self.signup = open(os.getcwd() + "\\assets\\signup.html", 'r').read()
        self.dbrowser = open(os.getcwd() + "\\assets\\dbrowser.html", 'r').read()
        self.mbrowser = open(os.getcwd() + "\\assets\\mbrowser.html", 'r').read()
        self.settings = open(os.getcwd() + "\\assets\\settings.html", 'r').read()
        self.alink = open(os.getcwd() + "\\assets\\alink.html", 'r').read()
        self.pending = Map()

    def get_bview(self):
        return self.dbrowser

    def get(self, data, user: User = None, additional_data=None, pal=False):
        additional = str()
        if additional_data is not None:
            for route in additional_data:
                additional += '/' + route
        print(additional)
        if user is None:
            return [self.noperm, []]
        if data is None:
            return [f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NVPN - redirect</title>
</head>
<body>
<script type="text/javascript">window.location.replace("{'/go/' + user.get_encrypter().encrypt(user.get_latest())}");</script>
</body>
</html>""", ['content-type', 'text/html']]

        try:
            if not pal:
                user.add_to_history(user.get_decrypter().decrypt(data) + additional)
            requester = Requester(user.get_decrypter().decrypt(data) + additional, user, pal)
            return requester.get_res()
        except:
            return ['error: DAU', ['Content-Type', 'text/html']]

    def get_page(self, data: str, user: User = None, args=None):
        if data == 'home':
            if user is None:
                return self.welcome
            print(data)
            return self.home
        elif data == 'go':
            if user is not None:
                return self.home
            return self.welcome
        elif data == 'login':
            return self.login
        elif data == 'settings':
            return self.settings
        elif data == 'alink':
            return self.alink
        elif data == 'signup':
            return self.signup
        elif data.startswith('open'):
            return f"""
                <!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
    <meta charset="UTF-8">
    <title>NVPN - redirect</title>
</head>
<body>
<script type="text/javascript">window.location.replace("{'/go/' + (user.get_encrypter().encrypt(args['data'])
                                                                                          if url.is_url(args['data'])
                                                                                          else user.get_encrypter().encrypt("https://www.google.com/search?q=" + args['data'].replace(' ', '+')))}");</script>
</body>
</html>
                """
        return '404'
