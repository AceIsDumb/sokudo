# requestss
import json
import asyncio
import os
import random
import requests
from PIL import Image
from io import BytesIO
from disnake.ext import commands
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.generativeai.types.generation_types import BlockedPromptException
from datetime import datetime
import re

# configure key
genai.configure(api_key=os.environ['GAI'])

# words to bad/replace
bad_words = {
    "@everyone": "@ everyone",
    "@here": "@ here",
    "skibidi": "sk*b*d*",
    "fuck": "f*ck",
    "shit": "sh*t",
    "bitch": "b*tch",
    "faggot": "f*ggot",
    "sex": "s*x",
    "nigga": "n*gga",
    "nigger": "n*gger",
    "niga": "n*ga",
    "niger": "n*ger"
}

# trigger words for the bot to respond to
triggers = [
    "kys", "kms", "kill yourself", "kill myself", "suicide", "depressed",
    "depression", "sad", "cry", "T^T", ":(", "die", "self-harm",
    "eating disorder", "bulimia", "anorexia", "hikikomori", "引き籠もり", "stupid",
    "dumb", "idiot", "useless", "retarded", "kill", "hit", "steal", "hurt",
    "harm", "harmful", "harmful", "harm", "blood", "worth", "wrong", "sokudo"
]


class AI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # set the chat model
        self.model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        # initialise the history
        self.chat = self.model.start_chat(history=[])
        # set the image model
        self.image_model = genai.GenerativeModel('gemini-1.5-pro')

    @commands.Cog.listener()
    async def on_message(self, message):
        # on message check for bad words
        g = ""
        e = message.content.lower()
        for i in e:
            if i.isalpha():
                g += i
        if any(t in g
               for t in bad_words.keys()) and not any(b in g
                                                      for b in triggers):
            await message.delete()
            return
        if message.author == self.bot.user or message.content.startswith("^"):
            return

        # replaces pings so that the bot knows who you are talking about
        content_with_names = self.replace_mentions_with_names(message)

        # tell it the time too
        current_datetime = datetime.now()
        current_date = current_datetime.strftime("%B %d, %Y")
        current_time = current_datetime.strftime("%I:%M %p")

        # if trigger words in it or mentioned or replied, respond
        if (message.guild is None or any(word in content_with_names.lower()
                                         for word in triggers)
                or (self.bot.user in message.mentions
                    and not message.mention_everyone)
                or (message.reference and message.reference.resolved
                    and message.reference.resolved.author == self.bot.user)):
            # clear history of messages after last 20 messages
            if len(self.chat.history) > 20:
                self.chat.history.pop(0)
            # start making prompt
            ask = (
                f"You are an API for a Discord chatbot (just return the response) that roleplays as Sokudo (速度), a 16-year-old Japanese girl with pink hair, born on August 1st, "
                f"Given a message from {message.author.display_name} "
                f"(actually {message.author.name}) in a Discord server on {current_date} at {current_time},"
            )

            # add context if message is a reply
            if message.reference and message.reference.resolved:
                resolved_author = message.reference.resolved.author
                ask += (
                    f" replying to {resolved_author.display_name} "
                    f"(actually {resolved_author.name}) message that says '{message.reference.resolved.content}',"
                )

            # manage attachments/images for prompt
            sample_files = []
            if message.attachments:
                for attachment in message.attachments:
                    if any(attachment.filename.lower().endswith(ext)
                           for ext in ["png", "jpg", "jpeg", "gif"]):
                        image_data = requests.get(attachment.url).content
                        image = Image.open(BytesIO(image_data))
                        sample_files.append(image)

            async with message.channel.typing():
                try:
                    if sample_files:
                        ask += (
                            " and attached these images. "
                            "(in brackets). Use informal text emojis sparingly, like ':)' or 'T^T'. Only provide the mental health resources when necessary. Use Singapore's Mental Health Resources by default"
                        )

                        ask += self.add_mental_health_resources(
                            content_with_names)
                        # use image model instead of chat model when there are images
                        response = self.image_model.generate_content(
                            [ask] + sample_files)
                    else:
                        # additional prompt instructions
                        ask += (
                            f" says: '{content_with_names}'. "
                            "(in brackets). Use informal text emojis sparingly, like ':)' or 'T^T'. Only provide the mental health resources when necessary. Use Singapore's Mental Health Resources by default"
                        )
                        ask += self.add_mental_health_resources(
                            content_with_names)
                        response = self.chat.send_message(
                            ask,
                            safety_settings={
                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:
                                HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                                HarmCategory.HARM_CATEGORY_HATE_SPEECH:
                                HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                                HarmCategory.HARM_CATEGORY_HARASSMENT:
                                HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
                                HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                            },
                        )
                # handle blocked prompts
                except BlockedPromptException:
                    await message.channel.send("I cannot reply to that...",
                                               reference=message,
                                               mention_author=False)
                    return
                except Exception as e:
                    print(f"Error generating response: {e}")
                    await message.channel.send(
                        "There was an error generating a response. Please try again later.",
                        reference=message,
                        mention_author=False)
                    return

            res = response.text
            # replace bad words
            for bad_word, replacement in bad_words.items():
                res = res.replace(bad_word, replacement)
            # break into chunks so that discord character limit doesn't affect it
            for chunk in self.break_string(res):
                await message.channel.send(chunk,
                                           reference=message,
                                           mention_author=False)
    
    def replace_mentions_with_names(self, message):
        # regex pattern for pings
        mention_pattern = r"<@(\d+)>"
        return re.sub(mention_pattern,
                      lambda m: self.get_display_name(m.group(1), message),
                      message.content)
    
    def get_display_name(self, user_id, message):
        # use discords api to get the user's display name
        user = message.guild.get_member(int(user_id))
        return f"{user.display_name} (actually {user.name})" if user else "<Unknown User>"

    def add_mental_health_resources(self, content):
        # add mental health resources to the prompt if needed
        with open("mhr.json", "r") as mhr_file:
            mhrr = json.load(mhr_file)

        resources = []
        for country, data in mhrr.items():
            for alias in data["Aliases"]:
                if alias in content:
                    resources.append(
                        f"{country}: {', '.join([f'{k} ({v})' for k, v in data['Data'].items()])}"
                    )
        return f" Mental health resources: {', '.join(resources)}." if resources else ""

    def break_string(self, s, max_length=4000):
        # separate into 4000 character strings
        return [s[i:i + max_length] for i in range(0, len(s), max_length)]


def setup(bot):
    bot.add_cog(AI(bot))
