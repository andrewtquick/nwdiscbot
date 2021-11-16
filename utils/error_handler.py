import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Context
from nextcord.ext.commands import MissingAnyRole, NoPrivateMessage

class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, err):
        if isinstance(err, MissingAnyRole):
            await ctx.send(f'Sorry {ctx.author.mention}, {err}', delete_after=20)
        if isinstance(err, NoPrivateMessage):
            await ctx.send(f"Sorry, I can't process that command via DM. Please use this command in the server.")
   
def setup(bot):
    bot.add_cog(ErrorHandler(bot))