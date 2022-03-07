import os
import cool_utils
import asyncio
import discord

from cool_utils import Terminal
from dotenv import load_dotenv, find_dotenv

from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

TOTAL_EXTENSIONS = []
LOADED_EXTENSIONS = []
UNLOADED_EXTENSIONS = [] 

load_dotenv(find_dotenv())

def get_loaded_extensions():
	for extension in LOADED_EXTENSIONS:
		choices = []
		class_ = Choice(name=extension, value=extension)
		choices.append(class_)
	return choices

def get_unloaded_extensions():
	for extension in UNLOADED_EXTENSIONS:
		choices = []
		class_ = Choice(name=extension, value=extension)
		choices.append(class_)
	return choices

def env(variable: str):
	env = os.getenv(variable)
	if env == None:
		Terminal.error(f"Environmental variable \"{variable}\" not found.")
		return None
	else:
		return env

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
		self.already_running = False

	async def start(self, *args, **kwargs):
		cool_utils.JSON.open('config')
		Terminal.start_log()
		await super().start(*args, **kwargs)

	async def close(self):
		Terminal.display("Gracefully Exiting Bot...")
		Terminal.stop_log()
		await super().close()

bot = Security()
command_tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
	embed_dict = build_embed("Bot Ready", "Security Bot Events", f"Bot has started.")
	if await log_event(embed_dict, bot=bot) == True:
		output("Bot Started.")
	else:
		output("Bot Started, Unable to log event.")
	if not bot.already_running:
		command_tree.sync()
	else:
		return
	bot.already_running = True

@app_commands.command(description="Checks if the bot is alive.")
async def alive(interaction):
	respond = interaction.response.send_message

	try:
		await respond(f":ballot_box_with_check: Security bot is alive!", ephemeral=True)
	except Exception as error:
		embed_dict = ("ERROR", "Security Bot Errors", f"```py\n{error}\n```")
		if await log_event(embed_dict, bot=bot) == True:
			output("An error occurred, Successfully logged error.")
		else:
			output("An error occurred, Unable to log error.")
		await respond(f":warning: An error has occurred while sending Ephemeral Message:\n\n```py\n{error}\n```")

@app_commands.command(description="Registers a user for authorising.")
@app_commands.describ(type="User role type.")
@app_commands.describ(user_id="User's Discord ID.")
async def register(interaction, type: str, user_id: str):
	respond = interaction.response.send_message
	author = interaction.user

	if owner(author) == False:
		return await respond(f":no_entry_sign: You don't have permissions to use this command.", ephemeral=True)
	if type.lower() == "guest":
		cool_utils.JSON.register_value(user_id, 'guests')
		await respond(f":ballot_box_with_check: Registered id `{user_id}` as `{type}`.", ephemeral=True)
	elif type.lower() == "privileged":
		cool_utils.JSON.register_value(user_id, 'privileged')
		await respond(f":ballot_box_with_check: Registered id `{user_id}` as `{type}`.", ephemeral=True)
	elif type.lower() == "developer":
		cool_utils.JSON.register_value(user_id, 'developer')
		await respond(f":ballot_box_with_check: Registered id `{user_id}` as `{type}`.", ephemeral=True)
	else:
		await respond(f":no_entry_sign: Invalid type!", ephemeral=True)

@app_commands.command(description="Unregisters a user from authorising.")
@app_commands.describ(user_id="Registered Discord User ID.")
async def unregister(interaction, user_id: str):
	respond = interaction.response.send_message
	author = interaction.user

	if owner(author) == False:
		return await respond(f":no_entry_sign: You don't have permissions to use this command.", ephemeral=True)
	if cool_utils.JSON.get_data(user_id) != "guest" and cool_utils.JSON.get_data(user_id) != "privileged":
		return await respond(f":ballot_box_with_check: Unregistered id `{user_id}`.")
	else:
		cool_utils.JSON.register_value(user_id, None)
		await respond(f":ballot_box_with_check: Unregistered id `{user_id}` from being `{type}`.", ephemeral=True)

@app_commands.command(description="Reloads a cog.")
@app_commands.describ(extension="Cog extension that needs to be reloaded.")
@app_commands.choices(extension=get_loaded_extensions())
async def reload(interaction, extension: str):
	respond = interaction.response.send_message
	author = interaction.user

	if owner(author) == False:
		return await respond(f":no_entry_sign: You don't have permission to use this command.", ephemeral=True)
	try:
		bot.unload_extension(f"cogs.{extension}")
		LOADED_EXTENSIONS.remove(extension)
		UNLOADED_EXTENSIONS.append(extension)
		bot.load_extension(f"cogs.{extension}")
		UNLOADED_EXTENSIONS.remove(extension)
		LOADED_EXTENSIONS.append(extension)
		output(f"Reloaded Cog \"{extension}\"")
		await respond(f":ballot_box_with_check: **`cogs.{extension}` reloaded.**", ephemeral=True)
	except Exception as error:
		output(f"An error occurred while reloading \"{extension}\" cog.")
		await respond(f":warning: An error occurred while reloading **`cogs.{extension}`**.\n\n```py\n{error}\n```", ephemeral=True)

@app_commands.command(description="Unloads a cog.")
@app_commands.describ(extension="Cog extension that needs to be unloaded.")
@app_commands.choices(extension=get_loaded_extensions())
async def unload(interaction, extension: str):
	respond = interaction.response.send_message
	author = interaction.user

	if owner(author) == False:
		return await respond(f":no_entry_sign: You don't have permission to use this command.", ephemeral=True)
	try:
		bot.unload_extension(f"cogs.{extension}")
		LOADED_EXTENSIONS.remove(extension)
		UNLOADED_EXTENSIONS.append(extension)
		output(f"Unloaded Cog \"{extension}\"")
		await respond(f":ballot_box_with_check: **`cogs.{extension}` unloaded.**", ephemeral=True)
	except Exception as error:
		output(f"An error occurred while unloading \"{extension}\" cog.")
		await respond(f":warning: An error occurred while unloading **`cogs.{extension}`**.\n\n```py\n{error}\n```", ephemeral=True)

@app_commands.command(description="Loads a cog.")
@app_commands.describ(extension="Cog extension that needs to be loaded.")
@app_commands.choices(extension=get_unloaded_extensions())
async def load(interaction, extension: str):
	respond = interaction.response.send_message
	author = interaction.user

	if owner(author) == False:
		return await respond(f":no_entry_sign: You don't have permission to use this command.", ephemeral=True)
	try:
		bot.load_extension(f"cogs.{extension}")
		UNLOADED_EXTENSIONS.remove(extension)
		LOADED_EXTENSIONS.append(extension)
		output(f"Reloaded Cog \"{extension}\"")
		await respond(f":ballot_box_with_check: **`cogs.{extension}` loaded.**", ephemeral=True)
	except Exception as error:
		output(f"An error occurred while loading \"{extension}\" cog.")
		await respond(f":warning: An error occurred while loading **`cogs.{extension}`**.\n\n```py\n{error}\n```", ephemeral=True)

@app_commands.command(description="Fetches updates from github and restarts the bot.")
async def fetch(interaction):
	respond = interaction.response.send_message
	author = interaction.user

	if owner(author) == False:
		return await respond(f":no_entry_sign: You don't have permission to use this command.", ephemeral=True)
	try:
		os.system(f"git pull")
		await respond(f"Fetched and updated from github, reloading bot now...", ephemeral=True)
		os.system(f"python3 index.py")
		await bot.logout()
	except Exception as error:
		await respond(f":warning: An error occurred while fetching updates and restarting.\n\n```py\n{error}\n```", ephemeral=True)

@app_commands.command(description="Pulls updates from Github")
async def pull(interaction):
	respond = interaction.response.send_message
	if owner(interaction.user) == False:
		return await respond(f":no_entry_sign: You don't have permission to use this command.", ephemeral=True)
	try:
		os.system("git pull")
		await respond(f":ballot_box_with_check: `$ git pull` executed with success.", ephemeral=True)
		command_tree.sync()
	except Exception as error:
		return await respond(f":warning: An error occurred while pulling github updates.\n\n```py\n{error}\n```", ephemeral=True)

def main():
	for file in os.listdir("./cogs"):
		if file.endswith(".py"):
			name = file[:-3]
			TOTAL_EXTENSIONS.append(file[:-3])
			try:
				bot.load_extension(f"cogs.{name}")
				LOADED_EXTENSIONS.append(name)
				output(f"\"{name}\" Cog Loaded.")
			except Exception as error:
				UNLOADED_EXTENSIONS.append(name)
				output(f"An error occurred while loading \"{name}\" cog.")
	bot.run(env("TOKEN"))

main()