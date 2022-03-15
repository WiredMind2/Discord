from user_api import User

if __name__ == "__main__":

    from token_secret import *

    # token = lynapse
    # token = deathwind
    token = will_i_am

    Account_Viewer(token)
    exit()
    user = User(token)
    print(user.getUserData())
    for g in user.getUserGuilds():
        print(g['id'], g['name'])

    guild = 724303646443044995  # TITANIUM
    # guild = 690519842830286859  # MMS
    # guild = 934746397767507978  # GoldenGamer321's Server
    # guild = 876018902004531231  # Zoo
    # guild = 881525113823047713  # Les Chayuns!
    # guild = 943886218192617522  # SDT


    # for k, v in user.getGuild(guild=guild).items():
    #     print(k, v)

    # invites = user.getGuildInvites(guild=guild)
    # if type(invites) == list:
    #     for i in invites:
    #         print(i['code'], ':', i['guild']['name'], '-', i['inviter']['username'])
    #         print(i)
    # else:
    #     print(invites)

    # bans = user.getGuildBans(guild=guild)
    # if type(bans) == list:
    #     for b in bans:
    #         print(b)
    # else:
    #     print(bans)

    for channel in user.getGuildChannels(guild=guild):
        print(channel['id'], channel['name'])

    # channel = 919183860376420363  # global-chat
    channel = 754316163705733171  # Bot testing

    # for msg in user.getChannelMessages(channel=channel)[::-1]:
    #     print(msg['author']['username'], msg['content'])

    msg = {
        'content': "Salut"
    }
    # print(user.createMessage(channel=channel, content=msg))

    #/!\ DANGEROUS /!\ -> Untested / Potential ban !!

    # owner = User(will_i_am)
    # guild_data = {
    #     'owner_id': owner.getUserData()['id']
    # }
    # print(user.modifyGuild(guild=guild, content=guild_data))