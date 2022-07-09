import os

import requests

from com.nosehad.python import url, logger
from com.nosehad.python.cookie import Cookie
from com.nosehad.python.replacer_c import ReplacerHtml
from com.nosehad.python.url_encrypter_c import UrlENC
from com.nosehad.python.user_c import User


class Requester:
    def __init__(self, turl, user: User, pal=False):

        self.pal = pal

        self.encrypter = user.get_encrypter()

        self.turl = turl

        self.cookies = user.get_cookies(url.get_raw(turl))

        self.format_cookies()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Cookie': self.cookies
        }

        self.req = requests.get(turl, headers=self.headers)
        if 'set-cookie' in self.req.headers:
            # print(self.req.headers['set-cookie'])
            for cookie in Cookie(self.req.headers['set-cookie']).get_cookies()[0]:
                user.set_cookie(url.get_raw(self.turl), cookie)
            for cookie in Cookie(self.req.headers['set-cookie']).get_cookies()[1]:
                user.rem_cookie(url.get_raw(self.turl), cookie)

        # print(user.get_cookies(self.turl))

    def format_cookies(self):
        if self.cookies is None:
            return
        temp = self.cookies
        self.cookies = str()
        for cookie in temp:
            self.cookies += f"{cookie[0]}={cookie[1]}; "

    def get_res(self):
        header = ['Content-Type', self.req.headers['Content-Type']]
        if url.has_extension(self.turl):
            if url.get_extension(self.turl).endswith('css'):
                header[1] = "text/css"
            if header[1].startswith('image') or header[1].startswith('video'):
                content = self.req.content
                self.req.close()
                return [content, header]
            elif header[1].endswith('x-msdownloadl') or header[1].endswith('x-apple-diskimage') or header[1].endswith(
                    'zip'):
                content = self.req.content
                self.req.close()
                return [content, header]

        res = ReplacerHtml(self.req.text, self.turl, self.encrypter, self.pal).get_result()
        self.req.close()
        return [res, header]
