import discord
from discord.ext import commands
from discord.utils import get



rolls_channel_id = None
tempChannels = []

class tempVoice(commands.Cog):
    def __init__(self, bot, channel):
        self.bot = bot
        self.template_channel_ID = channel
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after): 

        #Check for template channel
        try:
            if after.channel.id == self.template_channel_ID:
                #Create Temp Channel and move person to it
                channel_name = member.name + "'s Channel"
                channel_category = get(after.channel.guild.channels,name = after.channel.category)
                temp_channel = (await after.channel.guild.create_voice_channel(channel_name))
                await temp_channel.edit(category = channel_category)
                await member.move_to(temp_channel)

                tempChannels.append(temp_channel)

        except:
            pass
        
        for channel in tempChannels:
            if len(channel.members) == 0:
                await channel.delete()
                tempChannels.remove(channel)
