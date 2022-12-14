import discord
from discord import embeds
from discord.ext import commands
from discord.ext.commands.errors import ChannelNotReadable
from discord.utils import get

class tempVoice(commands.Cog):

    def __init__(self, bot, template_channel):
        self.bot = bot
        self.template_channel_IDs = template_channel
        self.tempChannels = []

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after): 
        
        if after.channel != None:
            await self.check_after_channels(member, after.channel)
        
        if before.channel != None:
            await self.check_before_channels(member, before.channel)
                

    async def check_after_channels(self, member, after_channel):

        if after_channel.id == self.template_channel_IDs:
            await self.create_channel(member, after_channel)

    async def check_before_channels(self, member, before_channel):

        if before_channel.id in self.tempChannels and len(before_channel.members) == 0:
            await before_channel.delete()
            self.tempChannels.remove(before_channel.id)

    async def create_channel(self, member, template):

        temp_channel = await template.clone(name = f"{member.name}'s Channel")

        await temp_channel.edit(category = template.category)

        await member.move_to(temp_channel)

        self.tempChannels.append(temp_channel.id) 
            
