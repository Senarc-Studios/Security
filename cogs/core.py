import os
import sys
import discord
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def restart(ctx):
        await ctx.send(f":ballot_box_with_check: Restarting Bot...", ephemeral=True)
        os.system("python3 main.py")
        sys.exit()

def setup(bot):
    bot.add_cog(Core(bot))