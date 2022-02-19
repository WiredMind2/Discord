import requests

from webhook_secret import *

lynapse = {
    'username': "Lynapse",
    'avatar_url': "https://cdn.discordapp.com/avatars/428885634338521088/e8eee13a55d5b7302eefa6b09983270d.webp?size=80",
}

skillslesss = {
    'username': 'Skillslesss',
    'avatar_url': "https://cdn.discordapp.com/avatars/926157348853149776/9fc8ee2b35d01bb98ff994bf0b69e93a.webp?size=32"
}

exstander = {
    'username': 'Vassily',
    'avatar_url': "https://cdn.discordapp.com/avatars/367365898215882762/4ad9b1be7f2d3f0213a7f0be61d7d23e.webp?size=32"
}

data = {
    'content': ("lynapse sucks " * 2000)[:2000]
}

data |= lynapse  # Set user

import time
while True:
    a = requests.post(chat_webhook_url, data)
    if a.content != b'':
        print("\n", a.content)
    time.sleep(2)
    print(".", end="")
