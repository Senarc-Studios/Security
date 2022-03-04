import os
import cool_utils
import asyncio
import discord

from cool_utils import Terminal
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def env(variable: str):
	return os.getenv(f"{variable}")

async def log_event(
	json = None,
	bot = None
	):
	try:
		embed = discord.Embed(description='> **' + json["action"].upper() + "**\n\n" + json["description"], colour=0x2F3136)
		embed.set_author(name=json["header"])
		embed.set_footer(text="Security Bot", icon_url=bot.user.display_avatar)
		channel = await bot.fetch_channel(env("EVENTS"))
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
	Terminal.display(content)

def owner(author):
	if int(author.id) == int(env("OWNER")):
		return True
	else:
		return False

intents = discord.Intents.all()
intents.members = True

class Security(commands.Bot):
	def __init__(self):
		super().__init__(
			command_prefix="!",
			intents=intents,
			slash_commands=True,
			message_commands=True,
			case_insensitive=True
		)

	async def start(self, *args, **kwargs):
		cool_utils.JSON.open('config')
		Terminal.start_log()
		await super().start(*args, **kwargs)

	async def close(self):
		Terminal.display("Gracefully Exiting Bot...")
		Terminal.stop_log()
		await super().close()

bot = Security()

@bot.event
async def on_ready():
	embed_dict = build_embed("Bot Ready", "Security Bot Events", f"Bot has started.")
	if await log_event(embed_dict, bot=bot) == True:
		output("Bot Started.")
	else:
		output("Bot Started, Unable to log event.")

@bot.command(brief="Checks if the bot is alive.", aliases = ["ca", "test", "check-alive"])
async def alive(ctx):
	try:
		await ctx.send(f":ballot_box_with_check: Security bot is alive!", ephemeral=True)
	except Exception as error:
		embed_dict = ("ERROR", "Security Bot Errors", f"```py\n{error}\n```")
		if await log_event(embed_dict, bot=bot) == True:
			output("An error occurred, Successfully logged error.")
		else:
			output("An error occurred, Unable to log error.")
		await ctx.send(f":warning: An error has occurred while sending Ephemeral Message:\n\n```py\n{error}\n```")

@bot.command(brief="Registers a user for authorising.", message_command=False)
async def register(ctx, type: str, user_id: str):
	if owner(ctx.author) == False:
		return await ctx.send(f":no_entry_sign: You don't have permissions to use this command.", ephemeral=True)
	if type.lower() == "guest":
		cool_utils.JSON.register_value(user_id, 'guests')
		await ctx.send(f":ballot_box_with_check: Registered id `{user_id}` as `{type}`.", ephemeral=True)
	elif type.lower() == "privileged":
		cool_utils.JSON.register_value(user_id, 'privileged')
		await ctx.send(f":ballot_box_with_check: Registered id `{user_id}` as `{type}`.", ephemeral=True)
	else:
		await ctx.send(f":no_entry_sign: Invalid type!", ephemeral=True)

@bot.command(brief="Unregisters a user from authorising.", message_command=False)
async def unregister(ctx, user_id: str):
	if owner(ctx.author) == False:
		return await ctx.send(f":no_entry_sign: You don't have permissions to use this command.", ephemeral=True)
	if cool_utils.JSON.get_data(user_id) != "guest" and cool_utils.JSON.get_data(user_id) != "privileged":
		return await ctx.send(f":ballot_box_with_check: Unregistered id `{user_id}`.")
	else:
		cool_utils.JSON.register_value(user_id, None)
		await ctx.send(f":ballot_box_with_check: Registered id `{user_id}` as `{type}`.", ephemeral=True)

@bot.command(brief="Reloads a cog.", message_command=False)
async def reload(ctx, extension: str):
	if owner(ctx.author) == False:
		return await ctx.send(f":no_entry_sign: You don't have permission to use this command.", ephemeral=True)
	try:
		bot.reload_extension(f"cogs.{extension}")
		output(f"Reloaded Cog \"{extension}\"")
		await ctx.send(f":ballot_box_with_check: **`cogs.{extension}` reloaded.**", ephemeral=True)
	except Exception as error:
		output(f"An error occurred while reloading \"{extension}\" cog.")
		await ctx.send(f":warning: An error occurred while reloading **`cogs.{extension}`**.\n\n```py\n{error}\n```", ephemeral=True)

@bot.command(brief="Fetches updates from github and restarts the bot.", message_command=False)
async def fetch(ctx):
	if owner(ctx.author) == False:
		return await ctx.send(f":no_entry_sign: You don't have permission to use this command.", ephemeral=True)
	try:
		os.system(f"git pull")
		await ctx.send(f"Fetched and updated from github, reloading bot now...", ephemeral=True)
		os.system(f"python3 index.py")
		await bot.logout()
	except Exception as error:
		await ctx.send(f":warning: An error occurred while fetching updates and restarting.\n\n```py\n{error}\n```", ephemeral=True)

@bot.command(brief="Pulls updates from Github", message_command=False)
async def pull(ctx):
	if owner(ctx.author) == False:
		return await ctx.send(f":no_entry_sign: You don't have permission to use this command.", ephemeral=True)
	try:
		os.system("git pull")
		await ctx.send(f":ballot_box_with_check: `$ git pull` executed with success.", ephemeral=True)
	except Exception as error:
		return await ctx.send(f":warning: An error occurred while pulling github updates.\n\n```py\n{error}\n```", ephemeral=True)

def main():
	for file in os.listdir("./cogs"):
		if file.endswith(".py"):
			name = file[:-3]
			try:
				bot.load_extension(f"cogs.{name}")
				output(f"\"{name}\" Cog Loaded.")
			except Exception as error:
				output(f"An error occurred while loading \"{name}\" cog.")
	bot.run(env("TOKEN"))

main()