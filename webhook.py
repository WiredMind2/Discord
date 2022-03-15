import requests

from webhook_secret import *
from token_secret import *
from user_api import User

lynapse = {
    'username': "Lynapse",
    'avatar_url': "https://cdn.discordapp.com/avatars/428885634338521088/82a10565ebb22c980b291b9d3b4d539e.webp",
}

skillslesss = {
    'username': 'Skillslesss',
    'avatar_url': "https://cdn.discordapp.com/avatars/926157348853149776/9fc8ee2b35d01bb98ff994bf0b69e93a.webp"
}

exstander = {
    'username': 'Vassily',
    'avatar_url': "https://cdn.discordapp.com/avatars/367365898215882762/4ad9b1be7f2d3f0213a7f0be61d7d23e.webp"
}

adi = {
    'username': 'Adidas',
    'avatar_url': 'https://cdn.discordapp.com/avatars/797815007420219403/9e51e8d9d53acac1a7277c3d29264e78.webp'
}

def get_user(id):
    user = User(will_i_am).getUser(user=id)
    user_data = {
        'username': user['username'],
        'avatar_url': f'https://cdn.discordapp.com/avatars/{id}/{user["avatar"]}.webp'
    }
    return user_data


data = {
    'content': "test"
}


user = get_user(USER_IDS['mee6'])

data |= user  # Set user

import time
while True:
    a = requests.post(spammer_webhook_url, data)
    if a.content != b'':
        print("\n", a.content)
    time.sleep(2)
    print(".", end="")
    break