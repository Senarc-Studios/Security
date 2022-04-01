import sys
import discord

from discord import app_commands
from discord.ext import commands

from typing import Choice

from utils.globals import respond, author, owner, output

class Core(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(description="Reloads a cog.")
	@app_commands.describe(extension="Cog extension that needs to be reloaded.")
	@app_commands.choices(extension=get_loaded_extensions())
	async def reload(self, interaction, extension: Choice[str]):
		respond = interaction.response.send_message
		author = interaction.user

		if owner(author) == False:
			return await respond(f":no_entry_sign: You don't have permission to use this command.", ephemeral=True)
		try:
			self.bot.unload_extension(f"cogs.{extension}")
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

	@app_commands.command(description="Shuts down the bot.")
	async def shutdown(self, interaction: discord.Interaction):
		if owner(author(interaction)) == False:
			return await respond(interaction, f":no_entry_sign: You don't have permissions to use this command.", ephemeral=True)
		await respond(interaction, f":ballot_box_with_check: Bot Shutting Down...", ephemeral=True)
		sys.exit()

async def setup(bot):
	bot.add_cog(Core(bot))