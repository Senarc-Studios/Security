from distutils import extension
import sys
import discord

from discord import app_commands
from discord.ext import commands

from discord.app_commands import Choice

from utils.globals import respond, author, owner, output

UNLOADED_EXTENSIONS = []
LOADED_EXTENSIONS = []

class Core(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		for extension in self.bot.UNLOADED_EXTENSIONS:
			UNLOADED_EXTENSIONS.append(extension)

		for extension in self.bot.LOADED_EXTENSIONS:
			LOADED_EXTENSIONS.append(extension)

	async def get_loaded_extensions(self, interaction, current: str):
		if LOADED_EXTENSIONS == []:
			return [Choice(name="No Extensions", value="No Extensions")]
		return [
			app_commands.Choice(name=extension, value=extension)
			for extensions in LOADED_EXTENSIONS if current.lower() in extensions.lower()
		]

	async def get_unloaded_extensions(self, interaction, current: str):
		if UNLOADED_EXTENSIONS == []:
			return [Choice(name="No Extensions", value="No Extensions")]
		return [
			app_commands.Choice(name=extension, value=extension)
			for extensions in UNLOADED_EXTENSIONS if current.lower() in extensions.lower()
		]

	@app_commands.command(description="Reloads a cog.")
	@app_commands.describe(extension="Cog extension that needs to be reloaded.")
	@app_commands.autocomplete(extension=get_loaded_extensions)
	async def reload(self, interaction, extension: str):
		respond = interaction.response.send_message
		author = interaction.user

		if owner(author) == False:
			return await respond(f":no_entry_sign: You don't have permission to use this command.", ephemeral = True)
		try:
			await self.bot.unload_extension(f"cogs.{extension}")
			self.bot.LOADED_EXTENSIONS.remove(extension)
			self.bot.UNLOADED_EXTENSIONS.append(extension)
			await self.bot.load_extension(f"cogs.{extension}")
			self.bot.UNLOADED_EXTENSIONS.remove(extension)
			self.bot.LOADED_EXTENSIONS.append(extension)
			output(f"Reloaded Cog \"{extension}\"")
			await respond(f":ballot_box_with_check: **`cogs.{extension}` reloaded.**", ephemeral = True)
		except Exception as error:
			output(f"An error occurred while reloading \"{extension}\" cog.")
			await respond(f":warning: An error occurred while reloading **`cogs.{extension}`**.\n\n```py\n{error}\n```", ephemeral = True)

	@app_commands.command(description="Loads a cog.")
	@app_commands.describe(extension="Cog extension that needs to be loaded.")
	@app_commands.autocomplete(extension=get_unloaded_extensions)
	async def load(self, interaction, extension: str):
		respond = interaction.response.send_message
		author = interaction.user

		if owner(author) == False:
			return await respond(f":no_entry_sign: You don't have permission to use this command.", ephemeral = True)
		try:
			await self.bot.load_extension(f"cogs.{extension}")
			self.bot.UNLOADED_EXTENSIONS.remove(extension)
			self.bot.LOADED_EXTENSIONS.append(extension)
			output(f"Loaded Cog \"{extension}\"")
			await respond(f":ballot_box_with_check: **`cogs.{extension}` loaded.**", ephemeral = True)
		except Exception as error:
			output(f"An error occurred while loading \"{extension}\" cog.")
			await respond(f":warning: An error occurred while loading **`cogs.{extension}`**.\n\n```py\n{error}\n```", ephemeral = True)

	@app_commands.command(description="Unloads a cog.")
	@app_commands.describe(extension="Cog extension that needs to be unloaded.")
	@app_commands.autocomplete(extension=get_loaded_extensions)
	async def unload(self, interaction, extension: str):
		respond = interaction.response.send_message
		author = interaction.user

		if owner(author) == False:
			return await respond(f":no_entry_sign: You don't have permission to use this command.", ephemeral = True)
		try:
			await self.bot.load_extension(f"cogs.{extension}")
			self.bot.UNLOADED_EXTENSIONS.append(extension)
			self.bot.LOADED_EXTENSIONS.remove(extension)
			output(f"Unoaded Cog \"{extension}\"")
			await respond(f":ballot_box_with_check: **`cogs.{extension}` unloaded.**", ephemeral = True)
		except Exception as error:
			output(f"An error occurred while unloading \"{extension}\" cog.")
			await respond(f":warning: An error occurred while unloading **`cogs.{extension}`**.\n\n```py\n{error}\n```", ephemeral = True)

	@app_commands.command(description="Shuts down the bot.")
	async def shutdown(self, interaction: discord.Interaction):
		if owner(author(interaction)) == False:
			return await respond(interaction, f":no_entry_sign: You don't have permissions to use this command.", ephemeral = True)
		await respond(interaction, f":ballot_box_with_check: Bot Shutting Down...", ephemeral = True)
		sys.exit()

async def setup(bot):
	await bot.add_cog(Core(bot))