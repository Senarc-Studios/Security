import os
import discord
import utils
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from discord.ext.commands import errors

def output(content):
	import datetime
	time = datetime.datetime.now()
	print(time.strftime(f"[%H:%M:%S]: ") + content)

def env(variable: str):
	load_dotenv(find_dotenv())
	return os.getenv(variable)

class Log(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command(self, ctx):
		events = int(env("EVENTS"))
		_embed = discord.Embed(colour=0x2F3136)
		_embed.set_author(name="Security Bot Events")
		_embed.add_field(name="Event:", value=f"`ON_COMMAND`", inline=False)
		_embed.add_field(name="Command:", value=ctx.command, inline=False)
		_embed.add_field(name="User:", value=f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", inlin=False)
		_embed.add_field(name="Time:", value=f"{discord.Timestamp.now()}", inline=False)
		_embed.set_footer(text="Security Bot", icon_url=self.bot.user.display_avatar)
		await events.send(embed=_embed)

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, errors.CommandNotFound):
			return
		events = int(env("EVENTS"))
		events = await self.bot.fetch_channel(events)
		_embed = discord.Embed(colour=0x2F3136)
		_embed.set_author(name="Security Bot Events")
		_embed.add_field(name="Event:", value=f"`ON_COMMAND_ERROR`", inline=False)
		_embed.add_field(name="Command:", value=ctx.command, inline=False)
		_embed.add_field(name="Error:", value=f"```py\n{type(error) + '\n' + error + '\n' +  error.__traceback__}\n```", inline=False)
		_embed.add_field(name="User:", value=f"{ctx.author.name}#{ctx.author.discriminator}(`{ctx.author.id}`)", inlin=False)
		_embed.add_field(name="Time:", value=f"{discord.Timestamp.now()}", inline=False)
		_embed.set_footer(text="Security Bot", icon_url=self.bot.user.display_avatar)
		await events.send(embed=_embed)

def setup(bot):
	bot.add_cog(Log(bot))