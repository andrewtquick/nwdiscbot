import nextcord
import os
from datetime import datetime
from nextcord.ext import commands
from db.firebase import DBConnection

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.nwdb = DBConnection()
        self.ANN_CHANNEL = int(os.getenv('ANN_CHANNEL'))

    @commands.Cog.listener()
    async def on_ready(self):
        print('NWBot online.')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member.bot:
            return

        if payload.channel_id == self.ANN_CHANNEL: 
            chan = self.bot.get_channel(self.ANN_CHANNEL)
            msg = await chan.fetch_message(payload.message_id)
            embed = msg.embeds[0]

            if payload.emoji.name == '✅':
                self.attendees = self.nwdb.get_attendee(payload.message_id)
                if payload.member.id not in self.attendees:
                    attendees = []
                    if 'None' in self.attendees:
                        self.attendees.remove('None')
                        self.attendees.append(payload.member.id)
                        self.nwdb.add_attendee(payload.message_id, self.attendees)

                        for member in self.attendees:
                            user = await self.bot.fetch_user(member)
                            attendees.append(user.name)

                        embed.set_field_at(3, name='Attendees', value='\n'.join(g for g in attendees), inline=False)
                    else:
                        self.attendees.append(payload.member.id)
                        self.nwdb.add_attendee(payload.message_id, self.attendees)

                        for member in self.attendees:
                            user = await self.bot.fetch_user(member)
                            attendees.append(user.name)

                        embed.set_field_at(3, name='Attendees', value='\n'.join(g for g in attendees), inline=False)
                
            if payload.emoji.name == '❌':
                self.attendees = self.nwdb.get_attendee(payload.message_id)

                if payload.member.id in self.attendees:
                    self.attendees.remove(payload.member.id)
                    attendees = []

                    if len(self.attendees) == 0:
                        self.attendees.append('None')
                        self.nwdb.rem_attendee(payload.message_id, payload.member.id)
                        self.nwdb.add_attendee(payload.message_id, 'None')
                        embed.set_field_at(3, name='Attendees', value='None', inline=False)
                    else:
                        self.nwdb.rem_attendee(payload.message_id, payload.member.id)

                        for member in self.attendees:
                            user = await self.bot.fetch_user(member)
                            attendees.append(user.name)

                        embed.set_field_at(3, name='Attendees', value='\n'.join(g for g in attendees), inline=False)
        
            await msg.edit(embed=embed)
            await msg.remove_reaction(payload.emoji, payload.member)

        if payload.emoji.name == '🗑️':
            evn_type, author = self.nwdb.get_author(payload.message_id)
            author_name = await self.bot.fetch_user(author)
            if evn_type == 'cor' and payload.member.id == author:
                cancel_embed = nextcord.Embed(title="Event has been cancelled!", description=f'Cancelled by **{author_name.name}**', colour=nextcord.Colour.orange())
                cancel_embed.set_thumbnail(url='https://i.imgur.com/gbsKvaS.png')
                cancel_embed.add_field(name='❌ Cancelled', value='Entry has been disabled', inline=False)
                cancel_embed.add_field(name='Stay tuned!', value='There will be more events posted in the near future! Continue to monitor this channel for more events.', inline=False)
                cancel_embed.set_footer(text=f'Event cancelled by {payload.member.name} - {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}', icon_url=f'{payload.member.avatar}')
                await msg.clear_reactions()
                await msg.edit(embed=cancel_embed)
                self.nwdb.del_event(payload.message_id)
            elif evn_type == 'war' and payload.member.id == author:
                cancel_embed = nextcord.Embed(title="Event has been cancelled!", description=f'Cancelled by **{author_name.name}**', colour=nextcord.Colour.orange())
                cancel_embed.set_thumbnail(url='https://i.imgur.com/9XLDmCH.png')
                cancel_embed.add_field(name='❌ Cancelled', value='Entry has been disabled', inline=False)
                cancel_embed.add_field(name='Stay tuned!', value='There will be more events posted in the near future! Continue to monitor this channel for more events.', inline=False)
                cancel_embed.set_footer(text=f'Event cancelled by {payload.member.name} - {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}', icon_url=f'{payload.member.avatar}')
                await msg.clear_reactions()
                await msg.edit(embed=cancel_embed)
                self.nwdb.del_event(payload.message_id)
            else:
                await chan.send(f'{payload.member.mention} -> Sorry, only {author_name.mention} can delete this event.')

def setup(bot):
    bot.add_cog(Events(bot))