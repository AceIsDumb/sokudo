import disnake
from disnake.ext import commands
import json
import os
from datetime import datetime
# journal filename
JOURNAL_FILE = 'journal.json'

class Journal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_journal_data()
    # load the data
    def load_journal_data(self):
        if os.path.exists(JOURNAL_FILE):
            with open(JOURNAL_FILE, 'r') as f:
                self.journal_data = json.load(f)
        else:
            self.journal_data = {}
    # save the data
    def save_journal_data(self):
        with open(JOURNAL_FILE, 'w') as f:
            json.dump(self.journal_data, f, indent=4)
    # add a new entry to the journal
    @commands.command()
    async def add_entry(self, ctx, *, entry: str):
        self.load_journal_data()
        user_id = str(ctx.author.id)
        if user_id not in self.journal_data:
            self.journal_data[user_id] = []

        entry_data = {
            'date': datetime.utcnow().isoformat(),
            'entry': entry
        }
        self.journal_data[user_id].append(entry_data)
        self.save_journal_data()
        await ctx.send(f"Journal entry added for {ctx.author.name}.")
    # see old entries
    @commands.command()
    async def view_entries(self, ctx):
        self.load_journal_data()
        user_id = str(ctx.author.id)
        if user_id not in self.journal_data or not self.journal_data[user_id]:
            await ctx.send("You have no journal entries.")
            return

        entries = self.journal_data[user_id]
        response = "Your journal entries:\n"
        for entry in entries:
            date = datetime.fromisoformat(entry['date']).strftime('%Y-%m-%d %H:%M:%S')
            response += f"[{date}] {entry['entry']}\n"
        
        await ctx.send(response)
    # delete all entries
    @commands.command()
    async def delete_entries(self, ctx):
        self.load_journal_data()
        user_id = str(ctx.author.id)
        if user_id in self.journal_data:
            self.journal_data[user_id] = []
            self.save_journal_data()
            await ctx.send(f"All journal entries deleted for {ctx.author.name}.")
        else:
            await ctx.send("You have no journal entries to delete.")

def setup(bot):
    bot.add_cog(Journal(bot))
