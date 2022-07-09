
import requests

from com.nosehad.python.crawler.crawler_c import WebCrawler
from com.nosehad.python.crawler.scanner_c import Scanner

# root = ET.fromstring(requests.get('fett=true').text)
# print(root.get('fett'))

# print(Scanner(requests.get('https://soracent.de').text, 'https://soracent.de').get_add())

WebCrawler(['https://youtube.com'])

def at(string, position, substring):
    for integer in range(len(substring)):
        print(integer)
        if string[position+integer] != substring[integer]:
            return False
    return True

# print(at('hello', 0, 'fello'))
