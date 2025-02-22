from disnake.ext import commands
import os

class Good(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Good is ready")

def setup(bot):
    bot.add_cog(Good(bot))
    # load actual stuffs
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f"cogs.Good.{filename[:-3]}")
