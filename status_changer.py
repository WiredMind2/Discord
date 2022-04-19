import datetime
import os
import sys
import time

from user_api import User

sys.path.append(os.path.abspath('../fichier/'))
from epub_parser import epub_parser


def change_status(text, delay=None):
    global user
    if delay is None:
        delay = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)).isoformat()

    data = {
        "custom_status": {
            "text": text,
            "expires_at": delay
        }
    }
    user.modifyUser(content=data)

def status_clock(delay=None):
    if delay is None:
        delay = 1

    while True:
        # tz = datetime.timedelta(hours=5, minutes=30)
        tz = datetime.timedelta(hours=4, minutes=0)
        tz = datetime.timezone(tz)
        t = datetime.datetime.now(tz).strftime('%H:%M:%S')
        out = change_status(t)
        if out is not None:
            print(f'{t} - {out}')
        else:
            print(t)
        time.sleep(1)

def text_lister(texts=None):
    if texts is None:
        texts = list(map(str, range(1, 11)))

    while True:
        for t in texts:
            change_status(t)
            print(f'Status: {t}')
            time.sleep(2)

def defiling_text(path=None):
    def line_iter(path):
        for line in epub_parser(path):
            while len(line) > 40:
                yield line[:40]
                line = line[40:]
            if line.strip() != '':
                yield line

    lines = []
    iterator = line_iter(path)
    while True:
        if len(lines) >= 3:
            lines.pop(0)
        while len(lines) < 3:
            lines.append(next(iterator))

        change_status(''.join(lines))
        time.sleep(2)

if __name__ == "__main__":

    from token_secret import *

    token = will_i_am

    user = User(token)

    defiling_text()

    # status_clock()
    # text_lister()
