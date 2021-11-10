import nextcord
import os
from datetime import datetime
from nextcord.ext import commands
from nextcord.ext.commands import command as Command

from db.firebase import DBConnection
from utils.utils import Utils

class War(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.attendees = ['None']
        self.announcer = None
        self.ANN_CHANNEL = os.getenv('ANN_CHANNEL')
        self.nwdb = DBConnection()
        self.utils = Utils(self)

    @Command(
        name='war',
        description="Announce Upcoming War Events\n\nlocation - Use location full name or abbrevation\ndate - Strictly use MM/DD format. Example: 11/12\ntime - 24hr EST time only. Example: 21:00",
        usage='<location> <MM/DD> <24hr EST time>'
        )
    async def war(self, ctx, *arg):
        user = await self.bot.fetch_user(ctx.author.id)
        date = arg[-2] + '/' + str(datetime.now().year)

        if self.utils.check_dt(date, arg[-1]):
            if len(arg) >= 3 and '/' in arg[-2] and ':' in arg[-1]:
                loc = ' '.join(l for l in arg[:-2])
                chan = self.bot.get_channel(int(self.ANN_CHANNEL))

                embed = nextcord.Embed(title="War has been declared!", description=f'Company war battle in {loc}', colour=nextcord.Colour.red())
                embed.set_thumbnail(url='https://i.imgur.com/9XLDmCH.png')
                embed.add_field(name='Date & Time', value=self.utils.convert_datetime(arg[-2], arg[-1]), inline=False)
                embed.add_field(name='Reminder', value='Upon joining, you will receive a notification 30mins before the start of the event..', inline=False)
                embed.add_field(name='Join & Leave Instructions', value='To **join**, click ✅\nTo **leave**, click ❌\nTo **Delete**, click 🗑️', inline=False)
                embed.add_field(name='Attendees', value='None', inline=False)
                embed.set_footer(text=f'Event created by {user.name} - {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}', icon_url=f'{user.avatar}')
                
                msg = await chan.send(embed=embed)
                await msg.add_reaction('✅')
                await msg.add_reaction('❌')
                await msg.add_reaction('🗑️')
                self.nwdb.new_event(msg.id, 'war', user.id, loc, arg[-2], arg[-1])
                self.nwdb.add_attendee(msg.id, 'None')
            else:
                await ctx.send(f"{user.mention} -> Something went wrong. Please use `--help war` for usage help.")
        else:
            await ctx.send(f"{user.mention} -> Can't create an event for a date and time in the past. Please use `--help invasion` for usage help.")


def setup(bot):
    bot.add_cog(War(bot))