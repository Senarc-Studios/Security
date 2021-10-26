import os
import utils
import discord
from discord.ext import commands

def output(content):
	import datetime
	time = datetime.datetime.now()
	print(time.strftime(f"[%H:%M:%S]: {content}"))

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(member):
		log = os.getenv("LOG")
		if utils.get_data('config', member.id) == "guests":
			try:
				role = discord.utils.get(member.guild.roles, id=os.getenv("GUEST_ROLE"))
				member.add_roles(role, reason="User registered as guest.")
				action = "Authorised as guest"
				code = "01AG"
			except:
				code = "ERAG"

		elif utils.get_data('config', member.id) == "privileged":
			try:
				role = discord.utils.get(member.guild.roles, id=os.getenv("PRIVILEGED_ROLE"))
				member.add_roles(role, reason="User registered as privileged")
				action = "Authorised as privileged"
				code = "01AP"
			except:
				code = "ERAG"

		else:
			try:
				embed = discord.Embed(description=f"You've joined **{member.guild.name}**, although you are not authorised as a guest or privileged. Please contact a administrator of Senarc if you think that this isn't what was meant to happen.", colour=0xFED42A)
				embed.set_author(name="Unauthorised Entry", icon_url="https://i.ibb.co/3YKyhxJ/black-exclamation-mark-on-yellow-260nw-1902354208-modified.png")
				embed.set_footer(text="Security Bot", icon_url=member.guild.me.display_avatar)
				await member.send(embed=embed)
				code = "01KU"
			except:
				code = "EMKU"
			try:
				await member.kick(reason=f"Unauthorised User.")
				action = "Kicked for being Unauthorised"
			except:
				action = "Kicked for being Unauthorised"
				code = "EUKU"

		_embed = discord.Embed(colour=0x2F3136)
		_embed.set_author(name="Security Bot Events")
		_embed.add_field(name="Action taken:", value=action)
		_embed.add_field(name="Action Code:", value=code)
		_embed.add_field(name="User:", value=f"{member.name}#{member.discriminator}(`{member.id}`)")
		await log.send(embed=_embed)

def setup(bot):
	bot.add_cog(Events(bot))