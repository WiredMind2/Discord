import json
import os
import sys
import time

from user_api import User

sys.path.append(os.path.abspath('../fichier/'))
from epub_parser import epub_parser


def readbook(path=None):
    book = epub_parser(path)
    buf = ''
    for line in book:
        if line.strip() == '':
            continue

        if len(buf) + len(line) > 2000:
            msg, buf = buf[:2000], buf[2000:]
            content = {
                'content':msg
            }
            out = user.createMessage(channel=CHANNEL, content=content)
            
            if out is not None:
                if type(out) is str:
                    try:
                        out = json.loads(out)
                    except:
                        pass
                if type(out) is str:
                    print('Not JSON:', type(out), '-', out)
                else:
                    if out.get('type') == 0:
                        pass
                    elif out.get('code') == 20028:
                        print(f'Waiting {out["retry_after"]} secs')
                        time.sleep(out['retry_after'])

        buf += line.strip()

if __name__ == "__main__":
    from token_secret import *

    token = will_i_am

    user = User(token)
    CHANNEL = 964880292269682708

    readbook()
