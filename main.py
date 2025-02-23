import disnake
from disnake.ext import commands
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
# set perms for bot
intents = disnake.Intents.all()
intents.members = True
intents.webhooks = True


# bad words for filter
bad_words = {
    "@everyone": "@ everyone",
    "@here": "@ here",
    "skibidi": "sk●b●d●",
    "fuck": "f●ck",
    "shit": "sh●t",
    "bitch": "b●tch",
    "faggot": "f●ggot",
    "sex": "s●x",
    "nigga": "n●gga",
    "nigger": "n●gger",
    "niga": "n●ga",
    "niger": "n●ger"
}

# set prefix
bot = commands.Bot(command_prefix="^", intents=intents)
GUILD_ID = []

# get absolute path for cogs
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
COGS_PATH = os.path.join(SCRIPT_DIR, "cogs")

# do stuff when bot's up
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user.name}")
    for g in bot.guilds:
        GUILD_ID.append(g.id)
        print(g.name)

    activity = disnake.Activity(
        type=disnake.ActivityType.playing,
        name="Disnake Dev",
        details="Under Development",
        timestamps={"start": 1722451200, "end": 1753987200},
        assets={"large_image": "pink", "large_text": "Sokudo", "small_image": "pink", "small_text": "Bot Level - 1"}
    )
    await bot.change_presence(activity=activity)

# load cogs (little parts of the bot)
def load_cogs():
    if not os.path.exists(COGS_PATH):
        print(f"cogs folder not found at: {COGS_PATH}")
        return
    
    for folder in os.listdir(COGS_PATH):
        folder_path = os.path.join(COGS_PATH, folder)
        if os.path.isdir(folder_path) and os.path.exists(os.path.join(folder_path, "__init__.py")):
            print(f"Sokudo Loaded: {folder}")
            bot.load_extension(f"cogs.{folder}")

# log commands
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
        description=f"Command: `{command_name}` \nUser: {user.display_name} ({user.name}) \nLocation: {location}"
    )

    logging_channel_id = 1274966435093024891
    logging_channel = bot.get_channel(logging_channel_id)
    if logging_channel:
        await logging_channel.send(embed=embed)

load_cogs()

# hello command
@bot.slash_command(name="hello", description="Say hello!", guild_ids=GUILD_ID)
async def hello_slash(inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_message(f"Hello, {inter.author.mention}!")

# load command
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"Loaded `{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"Failed to load cog `{extension}`.\n{e}")

# unload command
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"Unloaded `{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"Failed to unload cog `{extension}`.\n{e}")

# reload command
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"Reloaded `{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"Failed to reload cog `{extension}`.\n{e}")

# mimic command
@bot.command(name="mimic", help="mimic for good")
async def mimic(ctx, user: disnake.Member, *, message):
    if ctx.author.id != 996395908654694430:
        return
    await ctx.message.delete()
    channel = ctx.channel
    webhook = await channel.create_webhook(name='SOWebhook')

    avatar_urled = user.guild_avatar.url if user.guild_avatar else user.avatar.url
    user_display_name = user.nick if user.nick else user.display_name

    await webhook.send(content=message, username=user_display_name, avatar_url=avatar_urled)
    await webhook.delete()

# say command
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
        await ctx.send(message, files=attachments, reference=ctx.message.reference.resolved)
    else:
        await ctx.send(message, files=attachments)
    await ctx.message.delete()

# cogs list command
@bot.command()
@commands.is_owner()
async def cogs(ctx):
    if not os.path.exists(COGS_PATH):
        await ctx.send(f"❌ Cogs folder not found at: `{COGS_PATH}`")
        return

    cog_list = [f.replace('.py', '') for f in os.listdir(COGS_PATH) if os.path.isdir(os.path.join(COGS_PATH, f))]
    loaded_cogs = [cog for cog in bot.extensions]

    message = "●● Available Cogs: ●●\n"
    for cog in cog_list:
        status = "✅ Loaded" if f"cogs.{cog}" in loaded_cogs else "❌ Not Loaded"
        message += f"- `{cog}`: {status}\n"

    await ctx.send(message)

bot.run("KEY")