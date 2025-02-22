import disnake
from disnake.ext import commands
import os

ROLE_ID = 1268574774783643801  

class CodeCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="code", description="Code actions")
    async def code(self, ctx, filepath: str = None, *, code: str = None):
        # make sure they have role
        if not any(role.id == ROLE_ID for role in ctx.author.roles):
            await ctx.send("You do not have permission to use this command.")
            return

        # helper function to write data to a file and read it back
        def save_data(filen, data):
            with open(filen, "w") as write_file:
                write_file.write(data)
            with open(filen, "r") as read_file:
                datak = read_file.read()
            return datak

        # helper function to load data from a file
        def load_data(filen):
            try:
                with open(filen, "r") as read_file:
                    datad = read_file.read()
            except FileNotFoundError:
                return False  # return False if file not found
            return datad

        # helper function to list directory contents
        def list_directory(dir_path):
            try:
                items = os.listdir(dir_path)
            except FileNotFoundError:
                return False  # directory doesn't exist
            except NotADirectoryError:
                return None  # it's a file, not a directory
            return items

        # gets the file extension of a given path
        def get_file_extension(filepath):
            _, extension = os.path.splitext(filepath)
            return extension

        # ensures filepath is inside the bot's working directory
        def is_in_working_directory(filepath):
            cwd = os.getcwd()
            return os.path.commonpath([cwd, filepath]) == cwd

        # if no action is given, reject the request
        if code is None:
            await ctx.send("Code action not stated.")
            return

        # handle directory checking
        if code.startswith("check"):
            if filepath == "None":  # default to current directory
                filepath = os.getcwd()
            dir_contents = list_directory(filepath)
            if dir_contents is False:
                await ctx.send(f"No directory found at `{filepath}`")
                return
            elif dir_contents is None:
                await ctx.send(f"`{filepath}` is not a directory.")
                return

            # format output properly, or send as a file if too long
            output = f"Contents of `{filepath}`:\n" + "\n".join(dir_contents)
            if len(output) > 2000:
                with open("directory_contents.txt", "w") as f:
                    f.write(output)
                await ctx.send(f"Contents of `{filepath}`:", file=disnake.File("directory_contents.txt"))
                os.remove("directory_contents.txt")
            else:
                await ctx.send(f"Contents of `{filepath}`:\n```\n" + "\n".join(dir_contents) + "\n```")

        # handle file reading
        elif code.startswith("read"):
            if filepath is None:
                await ctx.send("Filepath not stated.")
                return
            absolute_path = os.path.abspath(filepath)
            await ctx.send(f"Attempting to read from `{absolute_path}`")
            file_content = load_data(absolute_path)
            if file_content is False:
                await ctx.send(f"No file found at `{filepath}` (absolute path: `{absolute_path}`)")
                return

            # send as a message or file if too long
            if len(file_content) > 2000:
                output_filename = "reading_" + str(os.path.basename(filepath))
                with open(output_filename, "w") as f:
                    f.write(file_content)
                await ctx.send(f"Content of `{filepath}`:", file=disnake.File(output_filename))
                os.remove(output_filename)
            else:
                await ctx.send(f"Content of `{filepath}`:\n```\n{file_content}\n```")

        # handle file writing
        elif code.startswith("write"):
            if filepath is None:
                await ctx.send("Filepath not stated.")
                return

            # check if user sent an attachment instead of inline code
            if not code[6:]:
                if len(ctx.message.attachments) > 0:
                    attachment = ctx.message.attachments[0]
                    await attachment.save(filepath)
                    await ctx.send(f"Saved attachment to `{filepath}`")
                else:
                    await ctx.send("No code provided and no attachment found.")
            else:
                code_content = code[6:]  # extract the actual code
                absolute_path = os.path.abspath(filepath)
                await ctx.send(f"Attempting to write to `{absolute_path}`")
                saved_content = save_data(absolute_path, code_content)
                await ctx.send(f"Saved code to `{filepath}`:\n```\n{saved_content}\n```")

        # handle file deletion
        elif code.startswith("delete"):
            if filepath is None:
                await ctx.send("Filepath not stated.")
                return
            absolute_path = os.path.abspath(filepath)
            os.remove(absolute_path)
            await ctx.send(f"Deleting `{filepath}` (absolute path: `{absolute_path}`)")

        else:
            await ctx.send("No valid command given. Use `check`, `read`, `delete` or `write`")

def setup(bot):
    bot.add_cog(CodeCommand(bot))
