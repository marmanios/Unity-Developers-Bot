import discord
from discord.ext import commands
from discord.ext.commands.errors import ChannelNotReadable
from discord.utils import get



rolls_channel_id = None
tempChannels = []

class tempVoice(commands.Cog):
    def __init__(self, bot, channel):
        self.bot = bot
        self.template_channel_IDs = [channel]
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after): 
        """
        print(before)
        print(after)
        print()
        print()
        """
        #Check for template channel
        try:
            if after.channel.id in self.template_channel_IDs:
                #Create Temp Channel and move person to it
                channel_name = member.name + "'s Channel"
                channel_category = after.channel.category
                temp_channel = (await after.channel.guild.create_voice_channel(channel_name))
                await temp_channel.edit(category = channel_category)
                await temp_channel.edit(sync_permissions = True)
                await member.move_to(temp_channel)
                tempChannels.append(temp_channel)

        except:
            pass
        
        for channel in tempChannels:
            if len(channel.members) == 0:
                await channel.delete()
                tempChannels.remove(channel)


    @commands.command()
    async def addTemplateChannel(self, ctx, id):
        for channel in ctx.guild.channels:
            if id == str(channel.id):
                self.template_channel_IDs.append(channel.id)
                await ctx.send('Added Channel: "{channel}" to Template Channel List'.format(channel=channel))
                return
        await ctx.send("Invalid channel ID")

    @commands.command()
    async def removeTemplateChannel(self, ctx, id):
        for channel in ctx.guild.channels:
            if (id == str(channel.id)) and (channel.id in self.template_channel_IDs):
                await ctx.send("Ey")
                self.template_channel_IDs.remove(int(id))
                await ctx.send("Removed Channel \"{channel}\" From Template Channel List".format(channel=ctx.guild.get))
                return
        
        await ctx.send("Invalid ID. You sent {id}".format(id = id))

    @commands.command()
    async def listTemplateChannels(self, ctx):
        for channelID in self.template_channel_IDs:
            channel = discord.utils.get(ctx.guild.channels, id=channelID)
            
            #Remove manually deleted template channels still in list
            if channel == None:
                self.template_channel_IDs.remove(channelID)
            else:
                await ctx.send(channel)
               
            
        
