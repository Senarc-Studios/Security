import os

from typing import List

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
