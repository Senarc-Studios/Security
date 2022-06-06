from motor.motor_asyncio import AsyncIOMotorClient

from discord import app_commands
from discord.ext.commands import GroupCog

from functions import get_db_users, Env

class User(
        GroupCog,
        prefix = "user"
    ):
    def __init__(self, bot):
        self.bot = bot
        self.USER_MONGO = AsyncIOMotorClient(Env.get("MONGO"))["senarc"]["users"]

    @app_commands.command(
        name = "info",
        description = "Get user information.",
    ):
    @app_commands.autocomplete(user = get_db_users)
    async def get_user_info(self, interaction, user: str):