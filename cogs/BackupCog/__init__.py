from disnake.ext import commands
import os

class BackupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("BackupCog is ready")

def setup(bot):
    bot.add_cog(BackupCog(bot))
    # load actual code
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f"cogs.BackupCog.{filename[:-3]}")
