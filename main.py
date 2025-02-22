import disnake
from disnake.ext import commands
import os
# set perms for bot
intents = disnake.Intents.all()
intents.members = True
intents.webhooks = True
# bad words for filter
bad_words = {
    "@everyone": "@ everyone",
    "@here": "@ here",
    "skibidi": "sk\*b\*d\*",
    "fuck": "f\*ck",
    "shit": "sh\*t",
    "bitch": "b\*tch",
    "faggot": "f\*ggot",
    "sex": "s\*x",
    "nigga": "n\*gga",
    "nigger": "n\*gger",
    "niga": "n\*ga",
    "niger": "n\*ger"
}
# set prefix
bot = commands.Bot(command_prefix="^", intents=intents)
GUILD_ID = []

# do stuff when bot's up
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}")
    for g in bot.guilds:
        GUILD_ID.append(g.id)
        print(g.name)
    # set bot activity
    activity = disnake.Activity(type=disnake.ActivityType.playing,
                                name="Disnake Dev",
                                details="Under Development",
                                timestamps={
                                    "start": 1722451200,
                                    "end": 1753987200
                                },
                                assets={
                                    "large_image": "pink",
                                    "large_text": "Sokudo",
                                    "small_image": "pink",
                                    "small_text": "Bot Level - 1"
                                })
    await bot.change_presence(activity=activity)

# load cogs (little parts of the bot)
def load_cogs():
    for folder in os.listdir("cogs"):
        if os.path.exists(os.path.join("cogs", folder, "__init__.py")):
            print(f"Sokudo Loaded: {folder}")
            bot.load_extension(f"cogs.{folder}")

# when command happens keep a log of them
@bot.event
async def on_command(ctx):
    command_name = ctx.command.name if ctx.command else 'Unknown'
    user = ctx.author
    channel = ctx.channel
    guild = ctx.guild.name if ctx.guild else 'DM'
    location = f"Guild: {guild}, Channel: {channel}" if guild != 'DM' else 'Direct Message'

    print(f"Command: '{command_name}' was used by {user} in {location}.")
    embed = disnake.Embed(
        title=f"Command {command_name} Used",
        description=
        f"Command: `{command_name}` \nUser: {user.display_name} ({user.name}) \nLocation: {location}"
    )

    logging_channel_id = 1274966435093024891
    logging_channel = bot.get_channel(logging_channel_id)
    if logging_channel:
        await logging_channel.send(embed=embed)


load_cogs()

# hello command to check if working
@bot.slash_command(name="hello", description="Say hello!", guild_ids=GUILD_ID)
async def hello_slash(inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_message(f"Hello, {inter.author.mention}!")

# load command to manual load, restricted to owner
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Loaded `{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"Failed to load cog `{extension}`.\n{e}")

# unload command to manual unload, restricted to owner
@bot.slash_command(name="say", description="Say something", guild_ids=GUILD_ID)
async def say_slash(inter: disnake.ApplicationCommandInteraction,
                    message: str = commands.Param(description="Message")):
    for t in bad_words.keys():
        message = message.replace(t, bad_words[t])
    await inter.response.send_message(f"{message}")

# unload command to manual unload, restricted to owner
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"Unloaded `{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"Failed to unload cog `{extension}`.\n{e}")

# reload command to manual reload, restricted to owner
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"Reloaded `{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"Failed to reload cog `{extension}`.\n{e}")



# mimic is a funny command to prank people
@bot.command(name="mimic", help="mimic for good")
async def mimic(ctx, user: disnake.Member, *, message):
    # no doing it on me
    if ctx.author.id != 996395908654694430:
        return
    # delete original command message
    await ctx.message.delete()
    # find channel
    channel = ctx.channel
    # make webhook
    webhook = await channel.create_webhook(name='SOWebhook')
    # log the name
    print(ctx.author.display_name)
    # log the user they want to mimic
    print(user)
    # find nickname 
    user_display_name = user.nick
    
    print(user.nick)
    # get avatar
    avatar_urled = user.guild_avatar
    # get avatar url if special for guild
    if avatar_urled != None:
        avatar_urled = user.guild_avatar.url
    else:
        # get global one if no special guild one
        avatar_urled = user.avatar.url
    print(avatar_urled)
    # no nickname then use normal username
    if user.nick == None:
        user_display_name = user.display_name
    # send message pretending to be person
    await webhook.send(
        content=message,
        username=user_display_name,
        avatar_url=avatar_urled
    )
    await webhook.delete()

# say command with filter
@bot.command()
@commands.is_owner()
async def say(ctx, *, message):
    attachments = []
    for t in bad_words.keys():
        message = message.replace(t, bad_words[t])
    if ctx.message.attachments:
        for a in ctx.message.attachments:
            af = await a.to_file()
            attachments.append(af)
    if ctx.message.reference and ctx.message.reference.resolved:
        await ctx.send(message,
                       files=attachments,
                       reference=ctx.message.reference.resolved)
    else:
        await ctx.send(message, files=attachments)
    await ctx.message.delete()


@bot.command()
@commands.is_owner()
async def cogs(ctx):
    cog_list = [
        f.replace('.py', '') for f in os.listdir('cogs')
        if os.path.isdir(os.path.join('cogs', f))
    ]
    loaded_cogs = [cog for cog in bot.extensions]

    message = "\*\*Available Cogs:\*\*\n"
    for cog in cog_list:
        status = "Loaded" if f"cogs.{cog}" in loaded_cogs else "Not Loaded"
        message += f"- {cog}: {status}\n"

    await ctx.send(message)


bot.run(os.environ['DKEY'])
