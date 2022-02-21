import os
import cool_utils
import discord

from cool_utils import Terminal
from dotenv import find_dotenv, load_dotenv
from discord.ext import commands

def output(content):
	Terminal.display(content)

def env(variable: str):
	load_dotenv(find_dotenv())
	return os.getenv(variable)

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member):
		log = int(env("LOG"))
		log = await self.bot.fetch_channel(log)
		if cool_utils.JSON.get_data(f"{member.id}") == "guests":
			try:
				role = discord.utils.get(member.guild.roles, id=int(env("GUEST_ROLE")))
				await member.add_roles(role, reason="User registered as guest.")
				action = "Authorised as guest"
				code = "01AG"
				output(f"Guest \"{member.name}\" joined.")
			except:
				action = "Authorised as guest"
				code = "ERAG"
				output(f"Guest \"{member.name}\" joined, Unable to give role.")

		elif cool_utils.JSON.get_data(f"{member.id}") == "privileged":
			try:
				role = discord.utils.get(member.guild.roles, id=int(env("PRIVILEGED_ROLE")))
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
		_embed.add_field(name="Action:", value=f"`ON_MESSAGE_JOIN`", inline=False)
		_embed.add_field(name="Action taken:", value=action, inline=False)
		_embed.add_field(name="Action Code:", value=f"`{code}`", inline=False)
		_embed.add_field(name="User:", value=f"{member.name}#{member.discriminator}(`{member.id}`)", inline=False)
		_embed.add_field(name="Time:", value=f"{discord.Timestamp.now()}", inline=False)
		_embed.set_footer(text="Security Bot", icon_url=member.guild.me.display_avatar)
		await log.send(embed=_embed)
	
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		output(f"User \"{member.name}\" left.")
		log = int(env("LOG"))
		log = await self.bot.fetch_channel(log)
		if member.leave_method == "kicked":
			code = "UK"
		elif member.leave_method == "banned":
			code = "UB"
		else:
			code = "UL"
		_embed = discord.Embed(colour=0x2F3136)
		_embed.set_author(name="Security Bot Events")
		_embed.add_field(name="Action:", value=f"`ON_MEMBER_REMOVE`", inline=False)
		_embed.add_field(name="Action Code:", value=code, inline=False)
		_embed.add_field(name="User:", value=f"{member.name}#{member.discriminator}(`{member.id}`)", inline=False)
		_embed.add_field(name="Time:", value=f"{discord.Timestamp.now()}", inline=False)
		_embed.set_footer(text="Security Bot", icon_url=member.guild.me.display_avatar)
		await log.send(embed=_embed)

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if message.content == "":
			return
		output(f"{message.author.name}'s Message got deleted.")
		log = int(env("LOG"))
		log = await self.bot.fetch_channel(log)
		_embed = discord.Embed(colour=0x2F3136)
		_embed.set_author(name="Security Bot Events")
		_embed.add_field(name="Action:", value=f"`ON_MESSAGE_DELETE`", inline=False)
		_embed.add_field(name="Action Content:", value=f"```\n{message.content.replace('`', '')}\n```", inline=False)
		_embed.add_field(name="User:", value=f"{message.author.name}#{message.author.discriminator}(`{message.author.id}`)", inline=False)
		_embed.add_field(name="Time:", value=f"{discord.Timestamp.now()}", inline=False)
		_embed.set_footer(text="Security Bot", icon_url=message.guild.me.display_avatar)
		await log.send(embed=_embed)

	@commands.Cog.listener()
	async def on_message_edit(self, original_message, edited_message):
		if original_message == "" or edited_message == "" or original_message.author.bot:
			return
		output(f"{original_message.author.name} Edited their message.")
		log = int(env("LOG"))
		log = await self.bot.fetch_channel(log)
		_embed = discord.Embed(colour=0x2F3136)
		_embed.set_author(name="Security Bot Events")
		_embed.add_field(name="Action:", value=f"`ON_MESSAGE_EDIT`", inline=False)
		_embed.add_field(name="Original Content:", value=f"```\n{original_message.content.replace('`', '')}\n```", inline=False)
		_embed.add_field(name="Edited Content:", value=f"```\n{edited_message.content.replace('`', '')}\n```", inline=False)
		_embed.add_field(name="User:", value=f"{original_message.author.name}#{original_message.author.discriminator}(`{original_message.author.id}`)", inline=False)
		_embed.add_field(name="Time:", value=f"{discord.Timestamp.now()}", inline=False)
		_embed.set_footer(text="Security Bot", icon_url=self.bot.user.display_avatar)
		await log.send(embed=_embed)

	@commands.Cog.listener()
	async def on_invite_create(self, invite):
		output(f"Auto-deleted a invite that was created by \"{invite.inviter.name}\".")
		log = int(env("LOG"))
		if cool_utils.JSON.get_data(f'{invite.inviter.id}') == 'notified':
			null = None
		else:
			embed = discord.Embed(description="Your Invite has been auto-deleted, you are not allowed to create invites since this is a private server.\n\nIf you want to invite someone to the server you should use https://api.senarc.org/authorise/lab this will help us identify if a user is authorised to join the server.\n\nIf you think this is a mistake, please contact a administrator.", colour=0xFED42A)
			embed.set_author(name="No Invites Allowed", icon_url="https://i.ibb.co/3YKyhxJ/black-exclamation-mark-on-yellow-260nw-1902354208-modified.png")
			embed.set_footer(text="Security Bot", icon_url=self.bot.user.display_avatar)
			await invite.inviter.send(embed=embed)
			utils.register_value(f'{invite.inviter.id}', 'notified')
		log = await self.bot.fetch_channel(log)
		_embed = discord.Embed(colour=0x2F3136)
		_embed.set_author(name="Security Bot Events")
		_embed.add_field(name="Action:", value=f"`ON_INVITE_CREATE`", inline=False)
		_embed.add_field(name="Action Taken:", value=f"`INVITE_DELETE`", inline=False)
		_embed.add_field(name="Invite Code:", value=f"`{invite.code}`", inline=False)
		_embed.add_field(name="Invite Channel:", value=f"<#{invite.channel.id}>", inline=False)
		_embed.add_field(name="User:", value=f"{invite.inviter.name}#{invite.inviter.discriminator}(`{invite.inviter.id}`)", inline=False)
		_embed.add_field(name="Time:", value=f"{discord.Timestamp.now()}", inline=False)
		_embed.set_footer(text="Security Bot", icon_url=self.bot.user.display_avatar)
		await invite.delete(reason="AUTO-DELETE-PROTECTION-RULE")
		await log.send(embed=_embed)

def setup(bot):
	bot.add_cog(Events(bot))