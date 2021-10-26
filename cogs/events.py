import os
import utils
import discord
from discord.ext import commands

def output(content):
	import datetime
	time = datetime.datetime.now()
	print(time.strftime(f"[%H:%M:%S]: ") + content)

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member):
		log = os.getenv("LOG")
		log = await self.bot.fetch_channel(log)
		if utils.get_data('config', f"{member.id}") == "guests":
			try:
				role = await member.guild.fetch_role(os.getenv("GUEST_ROLE"))
				await member.add_roles(role, reason="User registered as guest.")
				action = "Authorised as guest"
				code = "01AG"
				output(f"Guest \"{member.name}\" joined.")
			except:
				action = "Authorised as guest"
				code = "ERAG"
				output(f"Guest \"{member.name}\" joined, Unable to give role.")

		elif utils.get_data('config', f"{member.id}") == "privileged":
			try:
				role = await member.guild.fetch_role(os.getenv("PRIVILEGED_ROLE"))
				await member.add_roles(role, reason="User registered as privileged")
				action = "Authorised as privileged"
				code = "01AP"
				output(f"Privileged User \"{member.name}\" joined.")
			except:
				action = "Authorised as privileged"
				code = "ERAG"
				output(f"Privileged User \"{member.name}\" joined, Unable to give role.")

		else:
			try:
				embed = discord.Embed(description=f"You've joined **{member.guild.name}**, although you are not authorised as a guest or privileged. Please contact a administrator of Senarc if you think that this isn't what was meant to happen.", colour=0xFED42A)
				embed.set_author(name="Unauthorised Entry", icon_url="https://i.ibb.co/3YKyhxJ/black-exclamation-mark-on-yellow-260nw-1902354208-modified.png")
				embed.set_footer(text="Security Bot", icon_url=member.guild.me.display_avatar)
				await member.send(embed=embed)
				code = "01KU"
			except Exception:
				code = "EMKU"
			try:
				await member.kick(reason=f"Unauthorised User.")
				action = "Kicked for being Unauthorised"
			except Exception:
				action = "Kicked for being Unauthorised"
				code = "EUKU"

		_embed = discord.Embed(colour=0x2F3136)
		_embed.set_author(name="Security Bot Events")
		_embed.add_field(name="Action taken:", value=action, inline=False)
		_embed.add_field(name="Action Code:", value=code, inline=False)
		_embed.add_field(name="User:", value=f"{member.name}#{member.discriminator}(`{member.id}`)")
		await log.send(embed=_embed)

def setup(bot):
	bot.add_cog(Events(bot))