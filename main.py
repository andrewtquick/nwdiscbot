import nextcord
import os
from nextcord.ext import commands

bot = commands.Bot(command_prefix='--', intents=nextcord.Intents().all())

exts = [
    'cogs.corruption',
    'cogs.war',
    'utils.events',
    'cogs.tasks'
]

if __name__ == '__main__':
    for ext in exts:
        bot.load_extension(ext)

    bot.run(os.getenv('TOKEN'))