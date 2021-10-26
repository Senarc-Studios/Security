import os
import utils
import discord
import logging
from discord import commands
from .utils import log_event, build_embed

bot = commands.Bot(command_prefix="!", slash_interactions=True, message_commands=True)
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='[%H:%M:%S]: ')

@bot.event
async def on_ready():
	embed_dict = build_embed("Bot Ready", "Security Bot Events", f"Bot has started at {discord.Timestamp.now()}.")
	if log_event(embed_dict, bot=bot) == True:
		logging.info("Bot Started.")
	else:
		logging.info("Bot Started, Unable to log event.")

@bot.command(aliases = ["test", "check-alive"])
async def ca(ctx):
	try:
		await ctx.send(f":ballot_box_with_check: Security bot is alive!", ephemeral=True)
	except Exception as error:
		embed_dict = ("ERROR", "Security Bot Errors", f"```py\n{error}\n```")
		if log_event(embed_dict, bot=bot) == True:
			logging.info("An error occured, Successfully logged error.")
		else:
			logging.info("An error occured, Unable to log error.")
		await ctx.send(f":warning: An error has occured while sending Ephemeral Message:\n\n```py\n{error}\n```")

bot.run(utils.env("TOKEN"))