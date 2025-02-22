from disnake.ext import commands
import os

class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # 
    @commands.Cog.listener()
    async def on_ready(self):
        print("AICog is ready")

def setup(bot):
    bot.add_cog(AICog(bot))
    # load the actual code from file
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f"cogs.AICog.{filename[:-3]}")
