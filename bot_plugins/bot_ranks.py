#Discord_bot.py ranks module

import requests
import asyncio

import discord
from discord.commands.context import ApplicationContext
from discord.commands import Option

class Role_Management:
	"""Role management: role"""
	def initialize(self):
		txt_cmds = {
			self.update_roles: ['update_roles'],
			self.generate_roles: ['generate_roles']
		}

		self.ranks_ids = {
			10: 839779416326537237, # emerald
			9: 878564206025248788, # netherite
			8: 839779276924649472, # diamond
			7: 839771240066580500, # gold
			6: 839771165144121364, # redstone
			5: 839771065366347777, # lapis
			4: 839771007656001546, # iron
			3: 917778148798648321, # copper
			2: 839770919039402004, # coal
			1: 917774707049254982 # dirt
		}

		return txt_cmds

	async def update_roles(self, 
		ctx : ApplicationContext
		):
		"Update ranks for all members"

		ranks = {
			10: 30, # emerald
			9: 25, # netherite
			8: 20, # diamond
			7: 18, # gold
			6: 15, # redstone
			5: 13, # lapis
			4: 10, # iron
			3: 8, # copper
			2: 5, # coal
			1: 0 # dirt
		}

		try:
			members = ctx.guild.fetch_members()
		except HTTPException as e:
			print(f'Error on mary_all(): {e}')
			await ctx.respond('Error')
			return

		url = f'https://mee6.xyz/api/plugins/levels/leaderboard/{ctx.guild.id}'
		try:
			headers = {
				'Accept': 'application/json'
			}
			r = requests.get(url, headers=headers)

		except Exception as e:
			print(f'Error on Role_Management.roles(): {e}')
			ctx.respond('Error while fetching mee6 levels')
		else:
			data = r.json()
		level_data = {m['id']: m for m in data['players']}

		async for user in members:
			if user.bot:
				continue

			user_lvl = level_data.get(str(user.id), None)
			
			if user_lvl is None:
				# print(f'User {user.display_name}, id {user.id} not found in mee6 lvl data')
				continue

			new_rank = None
			for rank, lvl in ranks.items():
				if lvl <= user_lvl['level']:
					new_rank = rank
					break

			new_rank_id = self.ranks_ids[new_rank]

			to_remove = []
			add_role = True
			for role in user.roles:
				if role.id in self.ranks_ids.values():
					if role.id != new_rank_id:
						to_remove.append(role)
					else:
						add_role = False

			tasks = []
			if len(to_remove) > 0:
				t = user.remove_roles(*to_remove)
				tasks.append(t)

			if add_role:
				new_role = ctx.guild.get_role(new_rank_id)
				t = user.add_roles(new_role)
				tasks.append(t)
			
			try:
				await asyncio.gather(*tasks)
			except discord.Forbidden:
				print(f'Forbidden for user: {user.display_name}')
			else:
				if add_role:
					print(f'{new_role.name}: {user.display_name}, removed: {[r.name for r in to_remove]}')
				else:
					pass
					# print(f'OK: {user.display_name}, removed: {[r.name for r in to_remove]}')
	
	async def generate_roles(self, 
		ctx : ApplicationContext
		):
		"Generate roles from a list of rules (admin only!)"

		if ctx.author.id != self.admin:
			ctx.respond(f'Only the bot\'s admin can use this command!')

		perms = {
			1: [ # Dirt
				'connect',
				'external_emojis',
				'read_messages',
				'send_messages',
				'speak',
				'send_messages_in_threads',
				'use_voice_activation',
				'view_channel'
			],
			2: [ # Coal
				'add_reactions',
				'create_instant_invite',
				'embed_links',
				'read_message_history',
				'stream',
				'use_slash_commands'
			],
			3: [ # Copper
				'attach_files',
				'external_stickers',
				'request_to_speak'
			],
			4: [ # Iron
				'change_nickname',
				'send_tts_messages'
			],
			5: [ # Lapis
				'create_private_threads',
				'create_public_threads',
				'manage_nicknames'
			],
			6: [ # Redstone
				'manage_messages',
				'moderate_members',
				'mute_members'
			],
			7: [ # Gold
				'deafen_members',
				'move_members'
			],
			8: [ # Diamond
				'manage_threads',
				'priority_speaker'
			],
			9: [ # Netherite
				'manage_emojis',
				'manage_events',
				'start_embedded_activities'
			],
			10: [ # Emerald
				'manage_roles',
				'manage_webhooks',
				'view_audit_log'
			]
		}

		for rank in range(1, len(self.ranks_ids)+1):
			kwargs = {k: True for i in range(1, rank+1) for k in perms[i]}

			usr_perms = discord.Permissions.none()
			usr_perms.update(**kwargs)
			
			role_id = self.ranks_ids[rank]
			role = ctx.guild.get_role(role_id)


			try:
				await role.edit(permissions=usr_perms)
			except Forbidden:
				print(f'Forbidden for role: {role.name}')
			except HTTPException as e:
				print(f'Error for role: {role.name}, {e}')
			else:
				log_perms = False
				if log_perms:
					perms_txt = ' - ' + ', '.join(kwargs.keys())
				else:
					perms_txt = ''
				print(f'{role.name}: {len(kwargs)} perms{perms_txt}')


module_class = Role_Management