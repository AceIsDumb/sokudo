from disnake.ext import commands
import os

class Code(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Code is ready")

def setup(bot):
    bot.add_cog(Code(bot))
    # load actual code
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f"cogs.Code.{filename[:-3]}")
