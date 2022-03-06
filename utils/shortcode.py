import discord

def respond(interaction: discord.Interaction, message: str, ephemeral: bool=False):
    return interaction.response.send_message(message, ephemeral=True)

def author(interaction: discord.Interaction):
    return interaction.user