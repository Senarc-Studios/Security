import os
import sys
import discord
from discord.ext import commands

class Core(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(brief="Shuts down the bot.")
	async def shutdown(self, ctx):
		await ctx.send(f":ballot_box_with_check: Bot Shutting Down...", ephemeral=True)
		sys.exit()

def setup(bot):
	bot.add_cog(Core(bot))