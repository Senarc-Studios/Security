# import os
# import sys
# import discord

# from cool_utils import Terminal
# from utils.shortcode import respond, author
# from dotenv import load_dotenv, find_dotenv

# from discord import app_commands
# from discord.ext import commands

# def env(variable: str):
# 	load_dotenv(find_dotenv())
# 	env = os.getenv(variable)
# 	if env == None:
# 		Terminal.error(f"Environmental variable \"{variable}\" not found.")
# 		return None
# 	else:
# 		return env

# def owner(author):
# 	if int(author.id) == int(env("OWNER")):
# 		return True
# 	else:
# 		return False

# class Core(commands.Cog):
# 	def __init__(self, bot):
# 		self.bot = bot
	
# 	@tree.command(guild=CORE_GUILD, description="Shuts down the bot.")
# 	async def shutdown(self, inter: discord.Interaction):
# 		if owner(author(inter)) == False:
# 			return await respond(inter, f":no_entry_sign: You don't have permissions to use this command.", ephemeral=True)
# 		await respond(inter, f":ballot_box_with_check: Bot Shutting Down...", ephemeral=True)
# 		sys.exit()

# def setup(bot):
# 	bot.add_cog(Core(bot))