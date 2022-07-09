import datetime
import os
import threading
from time import strftime, gmtime

global instance


def get_logger():
    return instance


class Logger:
    def __init__(self):
        global instance
        instance = self
        self.file = open(os.getcwd() + f'\\logs\\{strftime("%Y-%m-%d--%H-%M-%S", gmtime())}.log',  "a", encoding="utf-8")
        self.log('Logger initialized!')

    def log(self, string):
        def _log():
            self.file.write(f"[{strftime('%H:%M:%S', gmtime())}] INFO: {string}\n")
            self.file.close()

        threading.Thread(target=_log).start()

    def save(self):
        self.file.write(self.cur)
        self.file.close()
