import nextcord
import os
from nextcord.ext import commands, tasks
from db.firebase import DBConnection
from utils.utils import Utils


class BotTasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.nwdb = DBConnection()
        self.utils = Utils(self)
        self.events = {}
        self.ANN_CHANNEL = int(os.getenv('ANN_CHANNEL'))
        
    @tasks.loop(minutes=1)
    async def getEvents(self):
        self.events = {}

        print('Getting events...')

        try:
            events = self.nwdb.get_event()

            for k in events.keys():
                if not k in self.events:
                    self.events.update(events)
        except:
            return
        else:
            await self.parse_events()
        
    async def parse_events(self):
        event_id = 0
        date = ''
        time = ''

        if self.events:
            for k, v in self.events.items():
                event_id = k
                date = v['date']
                time = v['time']

                if self.utils.within_start(date, time):
                    event = self.nwdb.get_specific_event(event_id)
                    attendees = event['attendees']
                    author_id = event['author_id']
                    event_type = event['type']
                    loc = event['location']
                    chan = self.bot.get_channel(self.ANN_CHANNEL)
                    msg = await chan.fetch_message(int(event_id))

                    if not 'None' in attendees:
                        for member in attendees:
                            user = await self.bot.fetch_user(int(member))
                            author = await self.bot.fetch_user(int(author_id))

                            if event_type == 'cor':
                                embed = nextcord.Embed(title='Corruption Event Reminder!!', description=f'This is your 30 minute reminder!', colour=nextcord.Colour.green())
                                embed.set_thumbnail(url='https://i.imgur.com/gbsKvaS.png')
                                embed.add_field(name='Location', value=f"{loc.title()}", inline=False)
                                embed.add_field(name='Date and Time', value=f"{date} - {time}", inline=False)
                                embed.set_footer(text=f'Event created by {author.name}', icon_url=f'{author.avatar}')

                                await msg.clear_reactions()
                                await msg.edit(embed=self.utils.complete_embed('cor', loc))

                            else:
                                embed = nextcord.Embed(title='Company War Event Reminder!!', description=f'This is your 30 minute reminder!', colour=nextcord.Colour.green())
                                embed.set_thumbnail(url='https://i.imgur.com/9XLDmCH.png')
                                embed.add_field(name='Location', value=f"{loc.title()}", inline=False)
                                embed.add_field(name='Date and Time', value=f"{date} - {time}", inline=False)
                                embed.set_footer(text=f'Event created by {author.name}', icon_url=f'{author.avatar}')

                                await msg.clear_reactions()
                                await msg.edit(embed=self.utils.complete_embed('war', loc))
                            
                            await user.send(embed=embed)
                            self.nwdb.del_event(event_id)
                    else:
                        await msg.clear_reactions()

                        if event_type == 'cor':
                            await msg.edit(embed=self.utils.complete_embed('cor', loc))
                        else:
                            await msg.edit(embed=self.utils.complete_embed('war', loc))

                        self.nwdb.del_event(event_id)

def setup(bot):
    bot.add_cog(BotTasks(bot))