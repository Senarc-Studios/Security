import os
import discord
import cool_utils

from cool_utils import Terminal
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands

def output(content):
	Terminal.display(content)

def env(variable: str):
	load_dotenv(find_dotenv())
	return os.getenv(variable)

class Log(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command(self, ctx):
		events = int(env("EVENTS"))
		events = await self.bot.fetch_channel(events)
		_embed = discord.Embed(colour=0x2F3136)
		_embed.set_author(name="Security Bot Events")
		_embed.add_field(name="Event:", value=f"`ON_COMMAND`", inline=False)
		_embed.add_field(name="Command:", value=f"`{ctx.command}`", inline=False)
		_embed.add_field(name="User:", value=f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", inline=False)
		_embed.set_footer(text="Security Bot", icon_url=self.bot.user.display_avatar)
		await events.send(embed=_embed)

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.errors.CommandNotFound):
			return
		e = "`"
		n = "\n"
		events = int(env("EVENTS"))
		events = await self.bot.fetch_channel(events)
		_embed = discord.Embed(colour=0x2F3136)
		_embed.set_author(name="Security Bot Events")
		_embed.add_field(name="Event:", value=f"`ON_COMMAND_ERROR`", inline=False)
		_embed.add_field(name="Command:", value=f"`{ctx.command}`", inline=False)
		_embed.add_field(name="Error:", value=f"{e}{e}{e}py{n}{error}{n}{error.__traceback__}{n}{e}{e}{e}", inline=False)
		_embed.add_field(name="User:", value=f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", inline=False)
		_embed.set_footer(text="Security Bot", icon_url=self.bot.user.display_avatar)
		await events.send(embed=_embed)
		raise error

def setup(bot):
	bot.add_cog(Log(bot))