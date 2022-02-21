import os
import sys
import discord
from discord.ext import commands

def env(variable: str):
	return os.getenv(f"{variable}")

def owner(author):
	if int(author.id) == int(env("OWNER")):
		return True
	else:
		return False

class Core(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(brief="Shuts down the bot.")
	async def shutdown(self, ctx):
		if owner(ctx.author) == False:
			return await ctx.send(f":no_entry_sign: You don't have permissions to use this command.", ephemeral=True)
		await ctx.send(f":ballot_box_with_check: Bot Shutting Down...", ephemeral=True)
		sys.exit()

def setup(bot):
	bot.add_cog(Core(bot))