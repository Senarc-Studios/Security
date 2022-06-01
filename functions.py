import os
import asyncio

from typing import List, enum
from discord.utils import get
from motor.motor_asyncio import AsyncIOMotorClient

from discord.app_commands import Choice

try:
	from cool_utils import Terminal
	from dotenv import load_dotenv, find_dotenv
except:
	os.system(f"ls -l; pip install -U -r requirements.txt")
	from cool_utils import Terminal
	from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Env:
	def __init__(self) -> None:
		pass

	@classmethod
	def get(self, variable):
		env = os.getenv(variable)
		if env == None:
			Terminal.error(f"Environmental variable \"{variable}\" not found.")
			return None
		else:
			return env

class Checks:
	def __init__(self) -> None:
		self.owners = [529499034495483926, 735369226063183932]
		self.privilegeds = []
		self.developers = []
		self.guests = []

	@classmethod
	def is_owner(self, id: int) -> bool:
		return id in self.owners
	
	@classmethod
	def is_developer(self, id: int) -> bool:
		return id in self.developers

	@classmethod
	def is_privileged(self, id: int) -> bool:
		return id in Env.get("PRIVILEGED")

	@classmethod
	def add_developers(self, ids: List[int]) -> None:
		for id in ids:
			self.developers.append(id)
		return None

	@classmethod
	def add_developer(self, id: int) -> None:
		self.developers.append(id)
		return None

	@classmethod
	def add_privilegeds(self, ids: List[int]) -> None:
		for id in ids:
			self.developers.append(id)
		return None

	@classmethod
	def add_privileged(self, id: int) -> None:
		self.privileged.append(id)
		return None

	@classmethod
	def add_guests(self, ids: List[int]) -> None:
		for id in ids:
			self.guests.append(id)
		return None

	@classmethod
	def add_guest(self, id: int) -> None:
		self.guests.append(id)
		return None

USER_MONGO = AsyncIOMotorClient(Env.get("MONGO"))["senarc"]["users"]

async def get_db_users(self, interaction, current: str) -> List[Choice]:
	users = await USER_MONGO.find({})
	return [
		Choice(
			name = user["discord"],
			value = int(user["discord_id"])
		)
		for user in users[:25] if current in user["discord_id"] or current in user["discord"]
	]

class Role(enum):
	OWNER = "owner"
	EXECUTIVE = "executive"
	MANAGER = "manager"
	DEVELOPER = "developer"
	COMMUNITY = "community"
