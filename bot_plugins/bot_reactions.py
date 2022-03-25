#Discord_bot.py reactions module

import discord
from discord.commands.context import ApplicationContext
from discord.commands import Option

class Simple_Reactions:
	"""Reactions: react"""
	def initialize(self):
		txt_cmds = {
			self.fill: ['fill'],
			self.unfill: ['unfill'],
			self.kiss: ['kiss'],
			self.welcome: ['welcome'],
			self.bang: ['bang'],
			self.hug: ['hug', 'hugs'],
			self.kick: ['kick'],
			self.punch: ['punch'],
			self.cry: ['cry'],
			self.lick: ['lick']
		}
		return txt_cmds

	async def fill(self, 
		ctx : ApplicationContext,
		up : Option(
			str,
			"'up' keyword",
			name="up",
			choices=['up'],
			required=True),
		target : Option(
			discord.Member,
			"The target to fill up.",
			name='target',
			required=True)
		):
		"Fill up someone (bruh)"

		if target.id == ctx.author.id:
			await ctx.respond(f'*{ctx.author.display_name} is filling up*')
		else:
			await ctx.respond(f'*{ctx.author.display_name} is filling {target.display_name}*')

	async def unfill(self, 
		ctx : ApplicationContext,
		target : Option(
			discord.Member,
			"The target to fill up.",
			name='target',
			required=True)
		):
		"Fill up someone (bruh)"

		if target.id == ctx.author.id:
			await ctx.respond(f'*{ctx.author.display_name} is getting unfilled*')
		else:
			await ctx.respond(f'*{ctx.author.display_name} is unfilling {target.display_name}*')

	async def kiss(self, 
		ctx : ApplicationContext,
		target : Option(
			discord.Member,
			"The target to kiss.",
			name='target',
			required=True)
		):
		"Kiss someone"

		if target.id == ctx.author.id:
			await ctx.respond(f'*{ctx.author.display_name} kisses himself?*')
		else:
			await ctx.respond(f'*{ctx.author.display_name} kisses {target.display_name}*')

	async def welcome(self, 
		ctx : ApplicationContext,
		target : Option(
			discord.Member,
			"The user to welcome.",
			name='user',
			required=True)
		):
		"Welcome someone"

		if target.id == ctx.author.id:
			await ctx.respond(f'*{ctx.author.display_name} welcomes himself?*')
		else:
			await ctx.respond(f'{ctx.author.display_name}: Welcome, {target.display_name} to T1T4N1UM Project!')

	async def bang(self, 
		ctx : ApplicationContext,
		target : Option(
			discord.Member,
			"The person to bang.",
			name='target',
			required=True)
		):
		"Bangs someone"

		if target.id == ctx.author.id:
			await ctx.respond(f'*{ctx.author.display_name} bangs himself?*')
		else:
			await ctx.respond(f'*{ctx.author.display_name} bangs {target.display_name}*')

	async def hug(self, 
		ctx : ApplicationContext,
		target : Option(
			discord.Member,
			"The person to hug.",
			name='target',
			required=True)
		):
		"Hugs someone"

		if target.id == ctx.author.id:
			await ctx.respond(f'*{ctx.author.display_name} is hugging himself, and starts crying...*')
		else:
			await ctx.respond(f'*{ctx.author.display_name} hugs {target.display_name}*')

	async def kick(self, 
		ctx : ApplicationContext,
		target : Option(
			discord.Member,
			"The person to kick.",
			name='target',
			required=True)
		):
		"Kicks someone"

		if target.id == ctx.author.id:
			await ctx.respond(f'*{ctx.author.display_name} kicks himself?*')
		else:
			await ctx.respond(f'*{ctx.author.display_name} kicks {target.display_name}*')

	async def punch(self, 
		ctx : ApplicationContext,
		target : Option(
			discord.Member,
			"The person to punch.",
			name='target',
			required=True)
		):
		"Punchs someone"

		if target.id == ctx.author.id:
			await ctx.respond(f'*{ctx.author.display_name} punches himself?*')
		else:
			await ctx.respond(f'*{ctx.author.display_name} punch {target.display_name} in the face!*')

	async def cry(self, 
		ctx : ApplicationContext,
		target : Option(
			discord.Member,
			"The person who made you cry.",
			name='target',
			default=None)=None
		):
		"Cries"

		if target is None:
			await ctx.respond(f'*{ctx.author.display_name} cries*')
		else:
			if target.id == ctx.author.id:
				await ctx.respond(f'*{ctx.author.display_name} cries on himself?*')
			else:
				await ctx.respond(f'*{ctx.author.display_name} is crying because of {target.display_name}!*')

	async def lick(self, 
		ctx : ApplicationContext,
		target : Option(
			discord.Member,
			"The person you want to lick.",
			name='target',
			default=None)=None
		):
		"Licks someone"

		if target.id == ctx.author.id:
			await ctx.respond(f'*{ctx.author.display_name} licks himself?*')
		else:
			await ctx.respond(f'*{ctx.author.display_name} licks {target.display_name}!*')


module_class = Simple_Reactions