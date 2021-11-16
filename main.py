import nextcord
import os
from nextcord.ext import commands

bot = commands.Bot(command_prefix='--', intents=nextcord.Intents().all(), help_command=None)

exts = [
    'cogs.corruption',
    'cogs.war',
    'cogs.tasks',
    'cogs.help',
    'utils.events',
    'utils.error_handler'
]

if __name__ == '__main__':
    for ext in exts:
        bot.load_extension(ext)

    bot.run(os.getenv('TOKEN'))