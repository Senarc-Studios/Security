import os
import discord

from cool_utils import Terminal

def respond(interaction: discord.Interaction, message: str, ephemeral: bool=False):
    return interaction.response.send_message(message, ephemeral = True)

def author(interaction: discord.Interaction):
    return interaction.user

def env(variable: str):
	env = os.getenv(variable)
	if env == None:
		Terminal.error(f"Environmental variable \"{variable}\" not found.")
		return None
	else:
		return env

def owner(user):
    if user.id == env("OWNER_ID"):
        return True
    return False

def output(content):
	Terminal.display(content)