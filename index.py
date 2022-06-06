import os
import sys
import asyncio
import discord
import cool_utils

from typing import Literal
from cool_utils import Terminal
from dotenv import load_dotenv, find_dotenv

from discord import app_commands
from discord.ui import View, Button, button
from discord.ext import commands
from discord.app_commands import Choice
from discord.ButtonStyle import gray, red, green, blue

from utils.globals import respond, author

TOTAL_EXTENSIONS = []
LOADED_EXTENSIONS = []
UNLOADED_EXTENSIONS = [] 
CORE_GUILD = discord.Object(id=902431960218075246)

button_cache = {}

load_dotenv(find_dotenv())

class Buttons(View):
	def __init__(self, command_name, message_id: int, bot, *, timeout = 30):
		super().__init__(timeout = timeout)
		self.bot = bot
		self.command_name = command_name
		self.bot.temp_var = None
		self.message_id = message_id

	@button(
		label = "Allow",
		style = green
	)
	async def allow(self, button: Button, interaction):
		for button_ in self.children:
			button_.disabled = True

		await interaction.response.edit_message(
			f"You've allowed {interaction.user.mention} to use the `/{self.command_name}` temporarily.",
			view = self
		)
		button_cache.update(
			{
				self.message_id: True
			}
		)

	@button(
		label = "Deny",
		style = red
	)
	async def deny(self, button: Button, interaction):
		for button_ in self.children:
			button_.disabled = True

		await interaction.response.edit_message(
			f"You've denied {interaction.user.mention} from using the `/{self.command_name}`.",
			view = self
		)
		button_cache.update(
			{
				self.message_id: False
			}
		)

def get_loaded_extensions():
	for extension in LOADED_EXTENSIONS:
		choices = []
		class_ = Choice(name=extension, value=extension)
		choices.append(class_)
	if len(LOADED_EXTENSIONS) == 0:
		return [Choice(name="No Extensions", value="No Extensions")]
	return choices

def get_unloaded_extensions():
	for extension in UNLOADED_EXTENSIONS:
		choices = []
		class_ = Choice(name=extension, value=extension)
		choices.append(class_)
	if len(UNLOADED_EXTENSIONS) == 0:
		return [Choice(name="No Extensions", value="No Extensions")]
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

intents = discord.Intents.all()
intents.members = True

async def sync_application(self):
	await self.tree.sync(guild=CORE_GUILD)
	Terminal.display("Application synced successfully.")

class Security(commands.Bot):
	def __init__(self):
		super().__init__(
			command_prefix="!",
			intents=intents,
			slash_commands=True,
			message_commands=True,
			case_insensitive=True,
			application_id=902464001101926450
		)
		self.already_running = False
		self.id = 902464001101926450
		self.LOADED_EXTENSIONS = []
		self.UNLOADED_EXTENSIONS = []

	async def owner(self, interaction):
		if int(interaction.author.id) == int(env("OWNER")):
			return True
		else:
			owner = await self.fetch_user(int(env("OWNER")))
			await interaction.response.edit_message(
				"Your request to access this owner only command has been sent to the owner, Please hold...",
				ephemeral = True
			)
			view = Buttons(
				command_name = interaction.command.name,
				bot = self,
				message_id = interaction.message.id
			)
			await owner.send(
				f"{interaction.user.mention} has requested to access `/{interaction.command.name}`.",
				view = view
			)
			await view.wait()
			return True if button_cache.get(interaction.message.id) is True else False

	async def start(self, *args, **kwargs):
		cool_utils.GlobalJSON.open('config')
		Terminal.start_log()
		await super().start(*args, **kwargs)

	async def close(self):
		Terminal.display("Gracefully Exiting Bot...")
		Terminal.stop_log()
		await super().close()

	async def setup_hook(self):
		for filename in os.listdir("./cogs"):
			if filename.endswith(".py"):
				name = filename[:-3]
				try:
					await bot.load_extension(f"cogs.{name}")
					self.LOADED_EXTENSIONS.append(name)
					output(f"\"{name}\" Cog Loaded.")
				except Exception as error:
					self.UNLOADED_EXTENSIONS.append(name)
					output(f"An error occurred while loading \"{name}\" cog.")
					print(error)

		self.loop.create_task(sync_application(self))

bot = Security()

@bot.event
async def on_ready():
	bot.already_running = True
	embed_dict = build_embed("Bot Ready", "Security Bot Events", f"Bot has started.")
	if await log_event(embed_dict, bot=bot) == True:
		output("Bot Started.")
	else:
		output("Bot Started, Unable to log event.")
	bot.tree.clear_commands(guild=None)
	output("Ensuring no global commands exists.")

@bot.tree.command(guild=CORE_GUILD, description="Shuts down the bot.")
async def shutdown(interaction: discord.Interaction):
	await interaction.send_message(
		"Processing command, please hold...",
		ephemeral = True
	)
	if await bot.owner(interaction = interaction) == False:
		return await interaction.response.edit_message(
			f":no_entry_sign: Your permission to use this command has been denied.",
			ephemeral = True
		)
	await interaction.response.edit_message(
		f":ballot_box_with_check: Bot Shutting Down...",
		ephemeral = True
	)
	sys.exit()

@bot.tree.command(guild=CORE_GUILD, description="Checks if the bot is alive.")
async def alive(interaction):
	await interaction.send_message(
		"Processing command, please hold...",
		ephemeral = True
	)

	try:
		await interaction.response.edit_message(
			f":ballot_box_with_check: Security bot is alive!",
			ephemeral = True
		)
	except Exception as error:
		embed_dict = ("ERROR", "Security Bot Errors", f"```py\n{error}\n```")
		if await log_event(embed_dict, bot=bot) == True:
			output("An error occurred, Successfully logged error.")
		else:
			output("An error occurred, Unable to log error.")
		await interaction.response.edit_message(f":warning: An error has occurred while sending Ephemeral Message:\n\n```py\n{error}\n```")

@bot.tree.command(guild=CORE_GUILD, description="Registers a user for authorising.")
@app_commands.describe(type="User role type.")
@app_commands.describe(user_id="User's Discord ID.")
async def register(interaction, type: Literal["guest", "developer", "privileged"], user_id: str):
	await interaction.response.send_message(
		"Processing command, please hold...",
		ephemeral = True
	)

	if await bot.owner(interaction = interaction) == False:
		return await interaction.response.edit_message(f":no_entry_sign: Your permission to use this command has been denied.", ephemeral = True)
	if type.lower() == "guest":
		cool_utils.GlobalJSON.register_value(user_id, 'guests')
		await interaction.response.edit_message(f":ballot_box_with_check: Registered id `{user_id}` as `{type}`.", ephemeral = True)
	elif type.lower() == "privileged":
		cool_utils.GlobalJSON.register_value(user_id, 'privileged')
		await interaction.response.edit_message(f":ballot_box_with_check: Registered id `{user_id}` as `{type}`.", ephemeral = True)
	elif type.lower() == "developer":
		cool_utils.GlobalJSON.register_value(user_id, 'developer')
		await interaction.response.edit_message(f":ballot_box_with_check: Registered id `{user_id}` as `{type}`.", ephemeral = True)
	else:
		await interaction.response.edit_message(
			f":no_entry_sign: Invalid type!",
			ephemeral = True
		)

@bot.tree.command(guild=CORE_GUILD, description="Unregisters a user from authorising.")
@app_commands.describe(user_id="Registered Discord User ID.")
async def unregister(interaction, user_id: str):
	await interaction.send_message(
		"Processing command, please hold...",
		ephemeral = True
	)

	if await bot.owner(interaction = interaction) == False:
		return await interaction.response.edit_message(f":no_entry_sign: Your permission to use this command has been denied.", ephemeral = True)
	_type = cool_utils.GlobalJSON.get_data(user_id, None)
	if _type == None:
		return await interaction.response.edit_message(f":no_entry_sign: Unable to find id `{user_id}`.", ephemeral = True)
	cool_utils.GlobalJSON.register_value(user_id, None)
	await interaction.response.edit_message(f":ballot_box_with_check: Unregistered id `{user_id}` from being `{_type}`.", ephemeral = True)

@bot.tree.command(guild=CORE_GUILD, description="Fetches updates from github and restarts the bot.")
async def fetch(interaction):
	await interaction.send_message(
		"Processing command, please hold...",
		ephemeral = True
	)

	if await bot.owner(interaction = interaction) == False:
		return await interaction.response.edit_message(f":no_entry_sign: Your permission to use this command has been denied.", ephemeral = True)
	try:
		os.system(f"git pull")
		await interaction.response.edit_message(f"Fetched and updated from github, reloading bot now...", ephemeral = True)
		os.system(f"python3 index.py")
		await bot.logout()
	except Exception as error:
		await interaction.response.edit_message(f":warning: An error occurred while fetching updates and restarting.\n\n```py\n{error}\n```", ephemeral = True)

@bot.tree.command(guild=CORE_GUILD, description="Pulls updates from Github")
async def pull(interaction):
	await interaction.send_message(
		"Processing command, please hold...",
		ephemeral = True
	)
	if await bot.owner(interaction = interaction) == False:
		return await interaction.response.edit_message(f":no_entry_sign: Your permission to use this command has been denied.", ephemeral = True)
	try:
		os.system("git pull")
		await interaction.response.edit_message(f":ballot_box_with_check: `$ git pull` executed with success.", ephemeral = True)
		await bot.tree.sync(guild=CORE_GUILD)
	except Exception as error:
		return await interaction.response.edit_message(f":warning: An error occurred while pulling github updates.\n\n```py\n{error}\n```", ephemeral = True)

if __name__ == "__main__":
	bot.run(env("TOKEN"))