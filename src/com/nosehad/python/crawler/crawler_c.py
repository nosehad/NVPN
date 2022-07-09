import json
import threading

import requests
from multiprocessing import Process

from com.nosehad.python.crawler.scanner_c import Scanner


class WebCrawler:
    def search(self, string):
        for uri in self.done:
            if string in uri:
                return uri

    def __init__(self, start_points):
        self.done = list()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Pragma': 'no-cache',
            'cookie': 'CONSENT=YES+yt.455245645.de+FX+022;',
            'Cache-Control': 'no-cache'
        }

        for url in start_points:
            threading.Thread(target=self.crawl, args=[url]).start()

    def crawl(self, url):
        if '?' in url or '=' in url or url in self.done or not (url.startswith('https://') or url.startswith('http://')):
            return
        if len(self.done) == 10000:
            open('./index.json', 'a').write(json.dumps(self.done))
            return
        req = requests.get(url, headers=self.headers)
        if 'html' not in req.headers['content-type']:
            return
        print('crawling', url)
        self.done.append(url)
        for uri in Scanner(req.text, url).get_result():
            try:
                threading.Thread(target=self.crawl, args=[uri]).start()
            except:
                pass



