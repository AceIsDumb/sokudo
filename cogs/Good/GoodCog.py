import random
import disnake
from disnake.ext import commands
import json
class GoodCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
				# pre-set affirmations
        self.affirmations = [
		    "You are capable of amazing things.",
		    "Believe in yourself and all that you are.",
  		  	"You are stronger than you think.",
  		  	"Every day is a second chance.",
 		  	"You are worthy of all the good things in life.",
  		  	"You are enough just as you are.",
  		  	"Your potential is endless.",
  		  	"You are doing your best, and that's enough.",
  		  	"You have the power to create change.",
  		  	"You are loved, you are valued, you are important.",
 		   	"You are capable of achieving your dreams.",
 		   	"You are resilient, brave, and strong.",
 		   	"You can handle whatever comes your way.",
 		   	"You are making a difference.",
		    "You are appreciated more than you know.",
		    "You have a beautiful mind and spirit.",
		    "You are growing and becoming your best self.",
		    "You are worthy of respect and acceptance.",
		    "You are surrounded by love and support.",
		    "You have the strength to overcome challenges.",
		    "You are worthy of happiness and joy.",
		    "You are unique and special.",
		    "You have the power to make positive changes.",
		    "You are a light in this world.",
		    "You have the ability to create the life you want.",
		    "You are more than enough.",
		    "You deserve to be happy and successful.",
		    "You are capable of handling difficult situations.",
		    "You are strong, intelligent, and capable.",
		    "You are worthy of love and respect.",
		    "You have the power to change your thoughts.",
		    "You are in control of your happiness.",
		    "You are brave for trying, and you are brave for caring.",
		    "You are doing better than you think.",
		    "You have the power to create your own happiness.",
		    "You are worthy of all the wonderful things in life.",
		    "You are important and your presence is needed.",
		    "You are worthy of achieving your goals.",
		    "You are capable of creating positive change.",
		    "You are worthy of love, respect, and kindness.",
		    "You are strong enough to face any challenge.",
		    "You are a wonderful person with so much to offer.",
		    "You are deserving of all the good things life has to offer.",
		    "You are doing an amazing job.",
		    "You are a positive influence on others.",
		    "You are a source of inspiration.",
		    "You have a kind heart and a beautiful mind.",
		    "You are worthy of taking time to rest and recharge.",
		    "You are a beacon of light to those around you.",
		    "You have the power to rise above any situation.",
		    "You are a valuable and irreplaceable person.",
		    "You are capable of finding solutions to any problem.",
		    "You are worthy of all the love and happiness in the world.",
		    "You have the strength to keep going.",
		    "You are worthy of the best that life has to offer.",
		    "You are doing a great job, keep it up.",
		    "You are enough, just as you are.",
		    "You are deserving of respect from yourself and others.",
		    "You have the ability to make your dreams come true.",
		    "You are a powerful creator.",
		    "You are capable of amazing things.",
		    "You have the power to make today a great day.",
		    "You are worthy of living a fulfilling life.",
		    "You are a beautiful person inside and out.",
		    "You have the power to make a difference.",
		    "You are worthy of achieving your dreams.",
		    "You are in control of your life.",
		    "You are strong, confident, and capable.",
		    "You are worthy of all the love and happiness in the world.",
		    "You are doing an amazing job.",
		    "You are worthy of all the good things in life.",
		    "You are capable of overcoming any obstacle.",
		    "You are worthy of living your best life.",
		    "You are enough just as you are.",
		    "You have the power to create positive change.",
		    "You are a light in this world.",
		    "You are deserving of happiness and success.",
		    "You are strong, intelligent, and capable.",
		    "You are worthy of love and respect.",
		    "You have the power to change your thoughts.",
		    "You are in control of your happiness.",
		    "You are brave for trying, and you are brave for caring.",
		    "You are doing better than you think.",
		    "You have the power to create your own happiness.",
		    "You are worthy of all the wonderful things in life.",
		    "You are important and your presence is needed.",
		    "You are worthy of achieving your goals.",
		    "You are capable of creating positive change.",
		    "You are worthy of love, respect, and kindness.",
		    "You are strong enough to face any challenge.",
		    "You are a wonderful person with so much to offer.",
		    "You are deserving of all the good things life has to offer.",
		    "You are doing an amazing job.",
		    "You are a positive influence on others.",
		    "You are a source of inspiration.",
		    "You have a kind heart and a beautiful mind.",
		    "You are worthy of taking time to rest and recharge.",
		    "You are a beacon of light to those around you.",
    		"You have the power to rise above any situation.",
    		"You are a valuable and irreplaceable person.",
   			"You are capable of finding solutions to any problem.",
    		"You are worthy of all the love and happiness in the world.",
    		"You have the strength to keep going.",
    		"You are worthy of the best that life has to offer."
		]
		# command
    @commands.command()
    async def affirmation(self, ctx):
				# love rng
        affirmation = random.choice(self.affirmations)
        await ctx.send(affirmation)
    # mental health resource look up
    @commands.command()
    async def mhr(self, ctx, *, nation: str = "singapore"):
        with open('mhr.json', 'r') as file:
            data = json.load(file)
        nation = nation.lower()
        title = "Mental Health Resources in "
        description = "A list of mentai health resources that you can use in "
        for c in data:
            if nation in data[c]["Aliases"]:
                title += c
                description += c
                datab = data[c]["Data"]
                for i in datab.keys():
                    description += f"\n**{i}**\n{datab[i]}\n"
                embed = disnake.Embed(title=title, description=description)
                await ctx.send(embed=embed)
                return
        await ctx.send(f"We are very sorry but {nation} is not stored in our data at the moment, please contact a developer about this")
                    
                

def setup(bot):
    bot.add_cog(GoodCog(bot))
	