import discord

from discord.commands.context import ApplicationContext
from discord.commands import Option

import random
import asyncio
import requests

from inspect import signature
from datetime import timedelta

import re
import time

import os
import json
import atexit

# import user_api
import bot_plugins

""" 
TODO:

- Settings save
- .welcome?

"""

class Commands(*bot_plugins.plugins):
	def __init__(self):
		self.txt_cmds = {
			self.set_activity: ['activity', 'set_activity'],
			self.block: ['ban', 'block', 'mute', 'set_ban', 'set_mute'],
			self.fight: ['battle', 'clash', 'fight', 'versus'],
			self.set_bot_mode: ['bot', 'botmode', 'set_bot', 'set_botmode'],
			self.choose: ['choose', 'which'],
			self.delete: ['del', 'delete', 'purge', 'remove', 'rm'],
			self.dice: ['dice', 'random'],
			self.help: ['doc', 'docs', 'help'],
			# self.embed: ['embed'],
			self.mention: ['find', 'match', 'mention', 'search'],
			self.swap_user: ['ghost', 'imitate', 'swap'],
			self.salute: ['hello', 'hey', 'hi', 'salute', 'test'],
			# self.image: ['image', 'img'],
			self.get_link: ['invite', 'link'],
			self.repeat: ['parrot', 'repeat'],
			self.ping: ['ping'],
			self.say: ['say'],
			self.set_shortcut: ['set'],
			self.set_status: ['set_status', 'status'],
			self.spam: ['spam'],
			self.stop: ['stop']
		}

		# self.txt_cmds = dict(sorted(((k, sorted(v)) for k, v in self.txt_cmds.items()), key=lambda e: e[1][0]))
		# print(self.txt_cmds)

		for p in bot_plugins.plugins:
			try:
				p_txt_cmds = p.initialize(self)
				# self.cmds |= {k:cmd for cmd, keys in p_txt_cmds.items() for k in keys}
				self.txt_cmds |= p_txt_cmds
			except:
				pass

		guild_ids = (e.id for e in self.guilds)
		for k,v in self.txt_cmds.items():
			self.slash_command(name=v[0], description=k.__doc__, guild_ids=[724303646443044995])(k)

		self.cmds = {k:cmd for cmd, keys in self.txt_cmds.items() for k in keys}

		# for self.repeat():
		if not hasattr(self, 'parrot_list'):
			self.parrot_list = []

		# for self.block():
		if not hasattr(self, 'banned_list'):
			self.banned_list = {}

		# for self.swap_user():
		if not hasattr(self, 'swaped_users'):
			self.swaped_users = {}

	async def salute(self, 
		ctx : ApplicationContext,
		user : Option(
			discord.Member,
            "The user to salute", 
            name="user",
            default=None)
		):
		"Helium is a very polite bot"
		if user is None:
			user = ctx.user
		txts = ['Hey {user}!', 'Hello {user}!', 'Good day to you, {user}!', 'Greetings, {user}, how are you today?']
		await ctx.respond(random.choice(txts).format(user=user.display_name))

	async def say(self, 
		ctx : ApplicationContext,
		content : Option(
			str,
            "The message to repeat", 
            name="message")
		):
		"Will repeat the content of your message:\n > .say I like pasta!"
		if len(content) == 0:
			await msg.channel.send('What am I supposed to say?')
			return
		a = ctx.send(content)
		b = ctx.delete()
		try:
			await asyncio.gather(a, b)
		except discord.NotFound as e:
			print(f'Error on .say: {e}')

	async def spam(self, 
		ctx : ApplicationContext,
		amount : Option(
			int,
            "Number of messages to send", 
            name="amount"),
		content : Option(
			str,
            "Message to send", 
            name="message"),
		delay : Option(
			int,
            "Delay between messages", 
            name="delay", 
            default=1),
		log_count : Option(
			bool,
			"Log the count of each message",
			default=True)
		):
		"Spam a message:\n > .spam 20 I like pasta!"
		if len(content) == 0:
			await ctx.respond('You need to specify a message to spam!')
			return

		pre = ''
		
		for i in range(amount):
			if log_count:
				pre = f'{i+1}: '
			try:
				await ctx.send(f'{pre}{content}')
			except Exception as e:
				print(f'Error while spamming (iter n{i+1}): {e}')
				break
			time.sleep(delay)

	async def dice(self, 
		ctx : ApplicationContext,
		hi : Option(
			int,
            "Max value", 
            name="max", 
            default=6), 
		lo : Option(
			str,
            "Min value", 
            name="min", 
            default=0)
		):
		"A random number:\n > .random\n > .random 50 100"
		if lo > hi:
			hi, lo = lo, hi
		num = random.randrange(lo+1, hi+1)

		entities = ['eggs', 'cars', 'children', 'cats', 'dogs', 'carrots']

		await ctx.respond(f'{num} {random.choice(entities)}')

	async def ping(self, 
		ctx : ApplicationContext,
		user : Option(
			discord.User,
			"User to ping",
			default=None)
		):
		"Ping the bot:\n > .ping\nAlso works like .mention:\n > .ping helium"
		if user is not None:
			return await self.mention(ctx, user)
		await ctx.respond(f"Pong: {round(self.latency*1000)}ms")

	async def delete(self, 
		ctx : ApplicationContext,
		msg_id : Option(
			str,
			"The id of the message to delete from",
			name="msg_id"),
		from_user : Option(
			discord.User,
			"Only delete messages from this user", 
            name="from",
			default=None)
		):
		"Purge all messages sent after the referenced message (from user):\n > .purge (@user)"
		
		await ctx.interaction.response.defer()
		if not ctx.interaction.channel.permissions_for(ctx.interaction.user).manage_messages:
			await ctx.respond("You don't have the 'Manage Messages' permission!")
			return

		msg = await ctx.fetch_message(msg_id)
		if msg is not None:
			beginning = msg.created_at
		else:
			# TODO - maybe use history()?
			await ctx.respond('Could not find the message!')
			return

		if from_user is not None:
			check = lambda e: e.id != ctx.interaction.id and e.author.id == from_user.id
		else:
			check = lambda e: e.id != ctx.interaction.id

		try:
			await ctx.interaction.channel.purge(check=check, after=beginning)	
		except discord.Forbidden:
			await ctx.respond("I don't have the 'Manage messages' permission!")
			return
		except discord.HTTPException as e:
			print(f"Error while purging the messages: {e}")
			await ctx.respond("Error while purging the messages")
			return

		date_txt = beginning.strftime('%d %b %Y, %H:%M')
		await ctx.channel.send(f'Purged messages since {date_txt}')

	async def help(self, 
		ctx : ApplicationContext
		):
		"Show Helium's help"
		docs = []
		for f, keys in self.txt_cmds.items():
			if f.__doc__ is not None:
				field = {
					'name': ' | '.join(map(lambda e: '.' + e, keys)),
					'value': f.__doc__
				}
				docs.append(field)

		emb = {
			"type": "rich",
			"title": "Helium's help",
			"description": "All commands available with Helium:",
			"color": 0x00FFFF,
			"fields": docs
		}

		emb = discord.Embed.from_dict(emb)
		await ctx.respond(embed=emb)

	async def mention(self, msg, *args):
		"Ping somebody:\n > .ping helium"
		if len(args) == 0:
			await msg.channel.send('You have to specify something to mention!')
			return
		elif len(args) > 1:
			for arg in args:
				await self.mention(msg, arg)
			return
		search = args[0].lower()

		match = discord.utils.find(lambda e: search in e.name.lower() and hasattr(e, 'mention'), (e for sub in (msg.guild.members, msg.guild.roles, msg.guild.channels) for e in sub))

		if match is None:
			await msg.channel.send(f'Nothing found for: {args[0]}!')
			return

		if hasattr(match, 'position') and match.position == 0:
			await msg.channel.send("You can ping @​everyone yourself! (I don't want any troubles)")
			return 
		await msg.channel.send(match.mention)

	async def choose(self, msg, *args):
		"If you have troubles making a decision:\n > .choose pasta pizza"
		if len(args) == 0:
			await msg.channel.send('I choose nothing?')
			return
		elif len(args) == 1:
			await msg.channel.send('Do I even have a choice??')
			return
		await msg.channel.send(f'I choose {random.choice(args)}!')

	async def fight(self, msg, *args):
		"Starts a pokemon-like fight:\n > .fight pikachu putin"
		args = list(args)
		if len(args) == 0:
			await msg.channel.send("You can't fight yourself??")
			return
		elif len(args) == 1:
			args.append(msg.author.display_name)

		for m in msg.mentions:
			if m.mention in args:
				args.remove(m.mention)
			args.append(m.display_name)

		fighters = {}
		for f in args:
			match = discord.utils.find(lambda e: f.lower() in e.name.lower() and hasattr(e, 'name'), (e for sub in (msg.guild.members, msg.guild.roles, msg.guild.channels) for e in sub))
			if match is not None:
				fighters[match.name] = 20
			else:
				fighters[f] = 20
		
		attacks = [
			'{f} uses a rock!',
			'{f} tries to run away!',
			'{f} uses his brain!',
			'{f} falls in love!',
			'{f} calls upon the soul of a dead warrior',
			'{f} falls asleep (zzz)',
			'{f} uses hacks!',
			'{f} need to go to the restroom!',
			'{f} fainted',
			'{f} is hungry??',
			'{f} farted',
			'{f} uses a tnt trap',
			'{f} is lagging',
			'{f} spams fireballs!'
		]

		effects = [
			('It\'s an instant kill!!', 10000),
			('It\'s very effective!', 10),
			('It did the job', 5),
			('It almost worked!', 3),
			('It could hurt a fly', 1),
			('It was useless...', 0)
		]

		round_embed = {
			"type": "rich",
			"title": 'Discord fight',
			"description": 'Round {i}',
			"color": 0x0000FF,
			"fields": [
				{
					"name": 'player1',
					"value": 'attacks',
					"inline": True
				},
				{
					"name": 'player2',
					"value": 'attack too',
					"inline": True
				},
			]
		}

		win_embed = {
			"type": "rich",
			"title": '{f} won!',
			"description": 'He had {h}hp left!',
			"color": 0x0000FF,
			"footer": {
				"text": 'use .fight to start another fight!'
			}
		}

		draw_embed = {
			"type": "rich",
			"title": 'Everybody died!',
			"description": 'Because no one won?',
			"color": 0x0000FF,
			"footer": {
				"text": 'use .fight to start another fight!'
			}
		}

		# fighters = {name: 20 for name in args}

		rounds = []
		
		while len(fighters) > 1:
			fight = []
			for fighter in fighters:
				target, health = random.choice([(f,h) for f, h in fighters.items() if f != fighter and h > 0])
				title = f'{fighter} chooses to attack {target}!'

				atk = random.choice(attacks)
				eff, dmg = random.choice(effects)
				txt = atk.format(f=fighter) + " - " + eff + f" ({dmg}hp): {target} now have {health-dmg}hp!"
				
				fighters[target] = health-dmg
				fight.append((title, txt))
				
				# await msg.channel.send(title)
				# await msg.channel.send(txt)
			fighters = {f: h for f, h in fighters.items() if h > 0}

			rounds.append(fight)

		for i, r in enumerate(rounds):
			fields = []
			for title, txt in r:
				fields.append({
					"name": title,
					"value": txt,
					"inline": True
					})
			round_embed["fields"] = fields
			round_embed["description"] = f"Round {i+1}"
			emd = discord.Embed.from_dict(round_embed)
			await msg.channel.send(embed=emd, reference=msg)

		if len(fighters) == 1:
			winner, health = list(fighters.items())[0]
			win_embed['title'] = win_embed['title'].format(f=winner)
			win_embed['description'] = win_embed['description'].format(h=health)

			emd = discord.Embed.from_dict(win_embed)
			await msg.channel.send(embed=emd, reference=msg)
			# await msg.channel.send(f'{winner} won with {health}hp!')
		else: #len(fighters) == 0
			# await msg.channel.send(f'Everyone died??')
			emd = discord.Embed.from_dict(draw_embed)
			await msg.channel.send(embed=emd, reference=msg)

	async def repeat(self, msg, *args):
		"Act like a parrot:\n > .repeat (start/stop/?) @user"
		if len(args) == 0:
			await msg.channel.send("You have to specify a user!")
			return

		force = False
		add = None

		if args[0] == "start":
			force = True
			add = True
		elif args[0] == "stop":
			force = True
			add = False

		for m in msg.mentions:
			if m.id == msg.author.id and not m.top_role.permissions.manage_messages:
				continue
			if (force and add) or m.id not in self.parrot_list:
				self.parrot_list.append(m.id)
				await msg.channel.send(f"I will now repeat {m.display_name}!")
				continue
			if (force and not add) or m.id in self.parrot_list:
				self.parrot_list.remove(m.id)
				await msg.channel.send(f"I will stop to repeat {m.display_name}")
				continue

	async def block(self, msg, *args):
		"Prevent someone from speaking:\n > .ban (start/stop/status) @user (5sec/2h/5days/...)"
		if len(args) == 0:
			await msg.channel.send("You have to specify a user!")
			return

		force = False
		add = None

		if args[0] == "start":
			force = True
			add = True
		elif args[0] == "stop":
			force = True
			add = False

		amount, unit, length = self.get_block_delay(args)

		for m in msg.mentions:
			if type(m) == discord.abc.User:
				await msg.channel.send(f'User not found: {m.display_name}')
				continue

			if not force:
				add = m.id not in self.banned_list

			if add:
				if msg.author.id != self.admin and msg.author.top_role.position < m.top_role.position:
					await msg.channel.send(f'You can\'t ban someone with a higher rank than you!')
					continue
				if m.bot or m.id == self.user.id:
					continue

				if length is not None:
					l_txt = f' ({amount} {unit})'
				else:
					l_txt = ''

				if m.id not in self.banned_list:
					self.banned_list[m.id] = length
				await msg.channel.send(f"{m.display_name}: **BANNED**{l_txt}")
				continue

			else:
				if msg.author.id != self.admin and msg.author.top_role.position < m.top_role.position:
					await msg.channel.send(f'You can\'t unban someone with a higher rank than you!')
					continue
				if m.id == msg.author.id and m.id != self.admin:
					continue

				if m.id in self.banned_list:
					del self.banned_list[m.id]
				await msg.channel.send(f"{m.display_name}: **UNBANNED**")
				continue

	def get_block_delay(self, args):
		units = {
			'month': 30,
			'day': 24,
			'hour': 60,
			'minute': 60,
			'second': 1
		} # Unit name and how many time the precedent one

		units = list(units.items())
		for i, d in list(enumerate(units))[::-1]:
			k, v = d
			if i < len(units)-1:
				v = units[i+1][1] * v
			units[i] = (k, v)

		units = dict(units) # Units in seconds

		unit_conv = {
			'month': ['month', 'months'],
			'day': ['d', 'day', 'days'],
			'hour': ['h', 'hour', 'hours'],
			'minute': ['m', 'min', 'mins', 'minute', 'minutes'],
			'second': ['s', 'sec', 'secs', 'second', 'seconds']
		}

		unit_conv = {k:v for v, keys in unit_conv.items() for k in keys} # Reversed dict

		amount, unit, length = None, None, None
		rgx = re.compile(r'(\d+)(\w+)')
		for arg in args:
			m = re.match(rgx, arg)
			if m:
				amount, unit = m.groups()
				amount, unit = int(amount), unit_conv[unit]
				length = int(amount) * units[unit]
				length += time.time()
				break

		return amount, unit, length

	async def unban(self, msg, *args):
		"Unban someone, equivalent to .ban stop @user"
		await self.block(msg, ['stop'] + args)

	async def get_link(self, msg, *args):
		"Please invite Helium in your server!"
		link = "https://discord.com/api/oauth2/authorize?client_id=720860720509485088&permissions=8&scope=bot"
		await msg.channel.send(f'Use this link to add me to your server! \n {link}')

	async def set_status(self, msg, *args):
		# "Allow to change Helium's status (check the API):\n > .status on field1 value1 field2 value2"
		if len(args) == 0:
			args.append("default")

		status_list = {
			discord.Status.online: ['online', 'default', 'on', 'green'],
			discord.Status.offline: ['offline', 'off', 'blank', 'none', None],
			discord.Status.idle: ['idle', 'moon', 'orange', 'sleep', 'sleeping'],
			discord.Status.dnd: ['dnd', 'stop', 'red'],
		}

		status_list = {n:s for s, names in status_list.items() for n in names}

		a = msg.channel.send(f"Settings status to {args[0]} - {status_list[args[0]]}")
		b = self.change_presence(status=status_list[args[0]])
		await asyncio.gather(a, b)

	async def set_activity(self, msg, *args):
		if len(args) == 0:
			args.append("default")

		activity_list = {
			discord.Game: {
				'txt': ['game', 'play'],
				'args': ['name'],
				'force': ['name']
			},
			discord.Streaming: {
				'txt': ['streaming', 'stream'],
				'args': ['platform', 'name', 'game', 'url'],
				'force': ['name', 'url']
			},
			discord.CustomActivity: {
				'txt': ['custom', 'special'],
				'args': ['name'],
				'force': ['name']
			},
			None: {
				'txt': ['default', 'none', None],
				'args': []
			}
		}

		txts = {txt: (act, data) for act, data in activity_list.items() for txt in data['txt']}

		action, *args = args

		if action not in txts:
			await msg.channel.send(f'Unknown activity: {action}')
			return

		act, data = txts[action]
		args = {args[i]:args[i+1] for i in range(0, len(args), 2)}
		for arg in args:
			if arg not in data['args']:
				await msg.channel.send(f'Invalid argument: {arg}!')
				return

		act = act(**args)

		print(act)

		a = msg.channel.send(f"Updating activity!")
		b = self.change_presence(activity=act)
		await asyncio.gather(a, b)

	async def set_bot_mode(self, msg, *args):
		"Bot mode: everyone get a 'bot' tag next to their name:\n > .bot on/off/status"
		if len(args) == 0:
			await msg.channel.send('You must specify an action (on/off/status)!')
			return
		else:
			mode = args[0]
	
		c_id = msg.channel.id

		if mode in ('on', 'enabled', 'start'):
			mode = True
		elif mode in ('off', 'disabled', 'stop'):
			mode = False
		elif mode in ('state', 'get', 'status'):
			mode = c_id in self.bot_mode
			status = "ENABLED" if mode else "DISABLED"
			await msg.channel.send(f'Bot mode: **{status}**')
			return
		else:
			await msg.channel.send(f'Invalid action: {mode} (on/off/status)!')
			return

		if mode:
			webhook = await self.get_webhook(msg.channel)
			perms = msg.channel.permissions_for(msg.guild.me)

			if webhook is None or not perms.manage_webhooks or not perms.manage_messages:
				await msg.channel.send("I need the 'Manage Webhooks' and 'Manage Messages' permissions to enable bot mode!")
				mode = False

			elif c_id not in self.bot_mode:
				self.bot_mode.append(c_id)
		else:
			if c_id in self.bot_mode:
				self.bot_mode.remove(c_id)

		if mode:
			await msg.channel.send('Bot mode: **ENABLED**')
		else:
			await msg.channel.send('Bot mode: **DISABLED**')

	async def swap_user(self, msg, *args):
		"While in bot mode, allow you to talk as someone else:\n > .swap @user"
		if msg.author.bot:
			await msg.delete()
		if msg.channel.id not in self.bot_mode:
			await msg.channel.send('You must activate bot mode first!')
			return

		if len(msg.mentions) == 0:
			del self.swaped_users[msg.author.id]

		target = msg.mentions[0]
		self.swaped_users[msg.author.id] = target

	async def set_shortcut(self, msg, *args):
		if len(args) == 0:
			await msg.channel.send('Invalid command')
			return

		cmd = f'set_{args[0]}'
		if cmd in self.cmds:
			return await self.cmds[cmd](msg, *args[1:])
		else:
			print(f'{msg.author.display_name} used an unknown command: {cmd}')

	async def embed(self, msg, *args):
		# "Generate an embed from json (debug tool)"
		try:
			embed = json.loads(' '.join(args))
			print(f'Generating embed from json: {embed}')

			emd = discord.Embed.from_dict(embed)
			await msg.channel.send(embed=emd, reference=msg)
		except Exception as e:
			print(f'Exception while generating embed: {e}')

	async def image(self, msg, *args):
		"Generate a preview from an image url:\n > .img link.url"

		if len(args) == 0:
			print('You must add a link!')

		url = args[0]

		emb = {
			'image': {
				'url': url,
			}
		}

		emb = discord.Embed.from_dict(emb)
		await msg.channel.send(embed=emb, reference=msg)

	async def stop(self, msg, *args):
		if msg.author.id != self.admin:
			await msg.channel.send("You are not allowed to stop the bot!")
			return
		await msg.channel.send("Bye!")
		await msg.channel.send("*Shutting down...*")
		await self.close()
		# self.exit_handler()
		exit()


class Bot(discord.Bot, Commands):
	def __init__(self, admin=None, prefix=None):
		self.settings_path = os.path.abspath('bot_settings')
		self.import_settings()

		atexit.register(self.save_settings)
		

		intents = discord.Intents().all()
		discord.Bot.__init__(self, intents=intents, command_prefix="(")

		Commands.__init__(self)
		
		if not hasattr(self, 'prefix'):
			if prefix == None:
				prefix = '.'
			self.prefix = prefix

		if not hasattr(self, 'admin'):
			if admin is not None:
				self.admin = admin
			else:
				raise ValueError("You must specify the admin's id at least once!")

		if not hasattr(self, 'webhooks'):
			self.webhooks = {}
		if not hasattr(self, 'bot_mode'):
			self.bot_mode = []

	async def on_ready(self):
		print(f'{self.user} is online!')

	async def on_disconnect(self):
		print(f'{self.user} disconnected!')

	async def on_message(self, msg):
		if self.user == msg.author or msg.author.bot:
			return

		if len(msg.embeds) > 0:
			for emb in msg.embeds:
				print(f'{msg.author.display_name}: {emb.to_dict()}')

		if msg.author.id != self.admin and msg.author.id in self.banned_list:
			if self.banned_list[msg.author.id] is not None and self.banned_list[msg.author.id] < time.time():
				print(f'Unbanned {msg.author.display_name} - time\'s up!')
				del self.banned_list[msg.author.id]
			else:
				await msg.delete()
				print(f'DELETED - {msg.author.display_name}: {msg.content}')
				return

		await self.check_bot_mode(msg)

		if msg.content.startswith(self.prefix):
			cmd = msg.content[len(self.prefix):].split()
			if cmd[0] in self.cmds:
				print(f'{msg.author.display_name} used the command: {cmd[0]}')
				f = self.cmds[cmd[0]]#(msg, *cmd[1:])
				print(f, signature(f)) # TODO
			else:
				print(f'{msg.author.display_name} used an unknown command: {cmd[0]}')
		else:
			if msg.author.id in self.parrot_list and msg.content != "":
				await msg.channel.send(msg.content, reference=msg)
			print(f'{msg.author.display_name}: {msg.content}')

	async def on_typing(self, channel, user, when):
		print(f'{user.display_name} is typing in {channel.name}')

	async def on_message_edit(self, before, after):
		print(f'Edited in channel {before.channel.name}, guild {before.guild.name}: {before.content} > {after.content}')

	async def on_message_delete(self, msg):
		if msg.channel.id in self.bot_mode and not msg.author.bot:
			return
		print(f'A message was deleted in channel {msg.channel.name}, guild {msg.guild.name}: {msg.content}')

	async def on_reaction_add(self, reaction, user):
		print(f'{user.display_name} added a reaction on: {reaction.message.content}')

	async def on_reaction_remove(self, reaction, user):
		print(f'{user.display_name} removed a reaction on: {reaction.message.content}')

	async def on_member_join(self, member):
		print(f'{member.display_name} just joined the guild {member.guild.name}!')

	async def on_member_remove(self, member):
		print(f'{member.display_name} just left the guild {member.guild.name}!')

	async def on_member_update(self, before, after):
		ignore = ['get_relationship']
		keys = ['activities', 'mobile_status', 'display_name', 'nick', 'name', 'pending', 'roles', 'desktop_status', 'web_status', 'status']
		changes = {k:getattr(after,k) for k in keys if getattr(before,k) != getattr(after,k)}
		# print(f'{after.name} just changed his profile on {after.guild.name}, changes:{changes}')

	async def on_user_update(self, before, after):
		keys = ['avatar', 'name', 'display_name', 'discriminator']
		changes = {k:getattr(after,k) for k in keys if getattr(before,k) != getattr(after,k)}
		print(f'{after.display_name} just changed his user, changes:{changes}')

	async def on_guild_role_create(self, role):
		print(f'New role created in guild {role.guild}: {role.name}')

	async def on_guild_role_delete(self, role):
		print(f'New role removed in guild {role.guild}: {role.name}')

	async def on_member_ban(self, guild, user):
		print(f'User {user.display_name} was banned from the guild {guild.name}')

	async def on_member_unban(self, guild, user):
		print(f'User {user.display_name} was unbanned from the guild {guild.name}')

	async def on_invite_create(self, invite):
		print(f'A new invite has been created for guild {invite.guild.name} by {invite.inviter.display_name}')

	#___________

	async def get_webhook(self, channel):
		c_id = channel.id
		if c_id in self.webhooks:
			hook = self.webhooks[c_id]
		else:
			try:
				hooks = await channel.webhooks()
			except discord.Forbidden:
				print(f'Error while fetching webhooks: Forbidden')
				return None
			if len(hooks) > 0:
				hook = hooks[0]
			else:
				avatar = await self.user.avatar_url.read()
				try:
					hook = await channel.create_webhook(
						name="Helium", 
						avatar=avatar,
						reason="Necessary to enable Helium's bot mode"
					)
				except discord.Forbidden:
					print(f'Error while creating webhook: Forbidden')
					return None
				except discord.HTTPException as e: # HTTPException
					print(f"Error while creating webhook: HTTPException - {e}")
					return None
				else:
					print(f'Created a webhook in channel {channel.name}, guild {channel.guild.name}')
			self.webhooks[c_id] = hook
		return hook

	async def check_bot_mode(self, msg):
		if msg.channel.id not in self.bot_mode:
			return

		if msg.author.bot:
			return

		if len(msg.attachments) > 0:
			return

		perms = msg.channel.permissions_for(msg.guild.me)
		if not perms.manage_webhooks or not perms.manage_messages:
			await msg.channel.send("I need the 'Manage Webhooks' and 'Manage Messages' permissions to enable bot mode!")
			return
		
		webhook = await self.get_webhook(msg.channel)
		if webhook is None:
			await self.cmds['bot'](msg, 'off')
			return

		user = self.swaped_users.get(msg.author.id, msg.author)

		data = {
			'content': msg.content,
			'username': (user.display_name),
			'avatar_url': f'https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.webp',
			'tts': msg.tts,
			'embeds': msg.embeds
		}
		a = msg.delete()
		b = webhook.send(**data)
		try:
			await asyncio.gather(a, b)
		except discord.HTTPException as e:
			print(f'Exception while using webhook {webhook.name}, channel {webhook.channel.name}: HTTPException - {e}')
			del self.webhooks[webhook.channel.id]
		except discord.NotFound:
			print(f'Exception while using webhook {webhook.name}, channel {webhook.channel.name}: NotFound')
			del self.webhooks[webhook.channel.id]

	def import_settings(self):
		if os.path.exists(self.settings_path):
			try:
				with open(self.settings_path, 'r') as f:
					data = json.load(f)
					for k, v in data.items():
						setattr(self, k, v)
			except:
				print('Error while importing settings!')

	def save_settings(self):
		keys = [
			'parrot_list',
			'banned_list',
			'prefix',
			'admin',
			'webhooks',
			'bot_mode'
		]

		data = {}
		for k in keys:
			data[k] = getattr(self, k)

		with open(self.settings_path, 'w') as f:
			json.dump(data, f)

		print('Saved settings!')

	def __enter__(self):
		return self

	def __exit__(self, *args):
		self.save_settings()


if __name__ == "__main__":
	from token_secret import *

	token = helium
	admin = will_i_am_id

	# bot = discord.Bot()

	# @bot.event
	# async def on_ready():
	#     print(f"We have logged in as {bot.user}")

	# # @bot.slash_command(guild_ids=[724303646443044995])
	# async def hello(ctx):
	#     await ctx.respond("Hello!")
	# bot.slash_command(guild_ids=[724303646443044995])(hello)

	# bot.run(token)

	with Bot(admin) as c:
		c.run(token)