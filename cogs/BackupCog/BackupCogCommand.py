import os
import shutil
from disnake.ext import commands
import disnake

class BackupCogCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.backup_folder = 'bot_backup'

    @commands.command()
    # make sure perms
    @commands.has_permissions(administrator=True)
    async def backup(self, ctx):
        # make backup folder
        zip_filename = f"{self.backup_folder}.zip"

        # check if backup folder exists
        if os.path.exists(self.backup_folder):
            shutil.rmtree(self.backup_folder)
        os.makedirs(self.backup_folder)

        # list with files to backup
        files_to_backup = []
        # go through all files
        for root, dirs, files in os.walk('.'):
            if '.git' in root:  
                continue
            for file in files:
                if file.endswith('.py') or file.endswith('.json') or file.endswith('.yml') or file.endswith('.log'):
                    file_path = os.path.join(root, file)

                    relative_path = os.path.relpath(file_path, start=os.getcwd())
                    files_to_backup.append((file_path, relative_path))


        for file_path, relative_path in files_to_backup:
            backup_path = os.path.join(self.backup_folder, relative_path)
            backup_dir = os.path.dirname(backup_path)
            os.makedirs(backup_dir, exist_ok=True)
            # copy file to archive
            shutil.copy(file_path, backup_path)

        # zip it
        shutil.make_archive(self.backup_folder, 'zip', self.backup_folder)

        
        with open(zip_filename, 'rb') as file:
            # give the backup
            await ctx.send("Here is the backup of the bot's code:", file=disnake.File(file, zip_filename))

        # delete the zip file and folder
        shutil.rmtree(self.backup_folder)
        os.remove(zip_filename)
        

def setup(bot):
    bot.add_cog(BackupCogCommand(bot))
