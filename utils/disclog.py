import discord
import utils

async def log_event(
	json = None,
	bot = None
	):
	try:
		embed = discord.Embed(description='> **' + json["action"].upper() + "**\n\n" + json["description"])
		embed.set_author(name=json["header"])
		embed.set_footer(text=json["footer"])
		channel = bot.fetch_channel(utils.env("EVENTS"))
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
		"description": description,
		"color": 0x2F3136,
		"footer": "Security Bot"
	}
	return BUILD_TEMPLATE