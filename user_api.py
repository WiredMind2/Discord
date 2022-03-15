import requests
import json


class User:
    def __init__(self, token=None):
        self.baseUrl = "https://discord.com/api/v9"
        self.token = token
        self.endpoints = {
            "getUserData": {
                "url": "/users/@me"
            },
            "getUser": {
                "url": "/users/{user}"
            },
            "getUserGuilds": {
                "url": "/users/@me/guilds"
            },
            "getGuild": {
                "url": "/guilds/{guild}"
            },
            "modifyGuild": {
                "url": "/guilds/{guild}",
                "method": "PATCH"
            },
            "getGuildChannels": {
                "url": "/guilds/{guild}/channels"
            },
            "getGuildMember": {
                "url": "/guilds/{guild}/members/{user}"  # DO NOT try to list members!!
            },
            "getGuildInvites": {
                "url": "/guilds/{guild}/invites"
            },
            "getGuildBans": {
                "url": "/guilds/{guild}/bans"
            },
            "getGuildBan": {
                "url": "/guilds/{guild}/bans/{user}"
            },
            "createGuildBan": {
                "url": "/guilds/{guild}/bans/{user}",
                "method": "PUT"
            },
            "removeGuildBan": {
                "url": "/guilds/{guild}/bans/{user}",
                "method": "DELETE"
            },
            "getChannel": {
                "url": "/channels/{channel}"
            },
            "getChannelMessages": {
                "url": "/channels/{channel}/messages"
            },
            "createMessage": {
                "url": "/channels/{channel}/messages",
                "method": "POST"
            },
            "deleteMessage": {
                "url": "/channels/{channel}/messages/{message}",
                "method": "DELETE"
            },
            "getChannelInvites": {
                "url": "/channels/{channel}/invites"
            },
            "createChannelInvite": {
                "url": "/channels/{channel}/invites",
                "method": "POST"
            },
            "getInvite": {
                "url": "/invites/{invite}",
                "method": "GET"
            }
        }

    def getHeader(self, content_type="application/json"):
        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        }
        if self.token:
            headers.update({"Authorization": self.token})
        return headers

    def API(self, url, method="GET", content={}, **kwargs):
        for k, v in kwargs.items():
            url = url.replace("{" + k + "}", str(v))
        url = self.baseUrl + url
        if method == "GET":
            r = requests.get(url, headers=self.getHeader())
        elif method == "POST":
            r = requests.post(url, data=json.dumps(content), headers=self.getHeader())
        elif method == "PATCH":
            r = requests.patch(url, data=json.dumps(content), headers=self.getHeader())
        elif method == "DELETE":
            r = requests.delete(url, headers=self.getHeader())
        else:
            raise Exception(str(method) + " is not supported!")
        return json.loads(r.content)

    def __getattr__(self, k):
        if k in self.__dict__['endpoints']:
            endpoint = self.__dict__['endpoints'][k]
            return lambda **kwargs: self.API(url=endpoint['url'], method=endpoint.get('method', 'GET'), **kwargs)
        else:
            print(self.__dict__)
            return self.__dict__[k]

    def token_checker(self, token):
        response = requests.get(self.baseUrl + '/auth/login', headers={"Authorization": token})
        return True if response.status_code == 200 else False

if __name__ == "__main__":
    from token_secret import *
    token = will_i_am
    u = User(token)