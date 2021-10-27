import os
import utils
import asyncio
import discord
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands

load_dotenv(find_dotenv())

async def log_event(
	json = None,
	bot = None
	):
	try:
		embed = discord.Embed(description='> **' + json["action"].upper() + "**\n\n" + json["description"], colour=0x2F3136)
		embed.set_author(name=json["header"])
		embed.set_footer(text="Security Bot", icon_url=bot.user.display_avatar)
		channel = await bot.fetch_channel(os.getenv("EVENTS"))
		await channel.send(embed=embed)
		return True
	except:
		return False

def build_embed(
	action = None,
	header = None,
	description = None
	):
	BUILD_TEMPLATE = {
		"action": action,
		"header": header,
		"description": description
	}
	return BUILD_TEMPLATE

def output(content):
	import datetime
	time = datetime.datetime.now()
	print(time.strftime(f"[%H:%M:%S]: {content}"))

def owner(author):
	if author.id == os.getenv("OWNER"):
		return True
	else:
		return False

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, slash_interactions=True, message_commands=True)

@bot.event
async def on_ready():
	embed_dict = build_embed("Bot Ready", "Security Bot Events", f"Bot has started at {discord.Timestamp.now()}.")
	if await log_event(embed_dict, bot=bot) == True:
		output("Bot Started.")
	else:
		output("Bot Started, Unable to log event.")

@bot.command(aliases = ["test", "check-alive"])
async def ca(ctx):
	try:
		await ctx.send(f":ballot_box_with_check: Security bot is alive!", ephemeral=True)
	except Exception as error:
		embed_dict = ("ERROR", "Security Bot Errors", f"```py\n{error}\n```")
		if await log_event(embed_dict, bot=bot) == True:
			output("An error occured, Successfully logged error.")
		else:
			output("An error occured, Unable to log error.")
		await ctx.send(f":warning: An error has occured while sending Ephemeral Message:\n\n```py\n{error}\n```")

@bot.command(message_command=False)
async def register(ctx, type: str, id: str):
	if not owner(ctx.author):
		return await ctx.send(f":no_entry_sign: You don't have permissions do use this command.", ephemeral=True)
	try:
		id = int(id)
	except:
		return await ctx.send(f":no_entry_sign: Invalid User ID.")
	if type.lower() == "guest":
		utils.register_value('config', id, 'guests')
		await ctx.send(f":ballot_box_with_check: Registered id `{id}` as `{type}`.", ephemeral=True)
	elif type.lower() == "privileged":
		utils.register_value('config', id, 'privileged')
		await ctx.send(f":ballot_box_with_check: Registered id `{id}` as `{type}`.", ephemeral=True)
	else:
		await ctx.send(f":no_entry_sign: Invalid type!", ephemeral=True)

@bot.command(message_command=False)
async def unregister(ctx, id: str):
	if not owner(ctx.author):
		return await ctx.send(f":no_entry_sign: You don't have permissions do use this command.", ephemeral=True)
	try:
		id = int(id)
	except:
		return await ctx.send(f":no_entry_sign: Invalid User ID.")
	if utils.get_data('config', id) != "guest" and utils.get_data('config', id) != "privileged":
		return await ctx.send(f":ballot_box_with_check: Unregistered id `{id}`.")
	else:
		utils.register_value('config', id, None)
		await ctx.send(f":ballot_box_with_check: Registered id `{id}` as `{type}`.", ephemeral=True)

def main():
	for file in os.listdir("./cogs"):
		if file.endswith(".py"):
			name = file[:-3]
			try:
				bot.load_extension(f"cogs.{name}")
				output(f"\"{name}\" Cog Loaded.")
			except Exception as error:
				output(f"An error occured while loading \"{name}\" cog.")
	bot.run(os.getenv("TOKEN"))

main()