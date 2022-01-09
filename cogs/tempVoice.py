import discord
from discord import embeds
from discord.ext import commands
from discord.ext.commands.errors import ChannelNotReadable
from discord.utils import get

class tempVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.template_channel_IDs = [925232981294063627]
        self.tempChannels = []
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after): 
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
                self.tempChannels.append(temp_channel)

        except:
            pass
        
        for channel in self.tempChannels:
            if len(channel.members) == 0:
                await channel.delete()
                self.tempChannels.remove(channel)


    @commands.command()
    async def addTemplateChannel(self, ctx, id):
        
        for channel in ctx.guild.channels:
            if id == str(channel.id) and channel.id not in self.template_channel_IDs:
                self.template_channel_IDs.append(channel.id)
                await ctx.send('Added Channel: "{channel}" to Template Channel List'.format(channel=channel))
                return

        await ctx.send("Invalid channel ID or Duplicate")

    @commands.command()
    async def removeTemplateChannel(self, ctx, id):
        for channel in ctx.guild.channels:
            if (id == str(channel.id)) and (channel.id in self.template_channel_IDs):
                self.template_channel_IDs.remove(int(id))
                channel_name = get(ctx.guild.channels, id=int(id))
                await ctx.send("Removed Channel \"{channel}\" From Template Channel List".format(channel= channel_name))
                return
        
        await ctx.send("Invalid ID. You sent {id}".format(id = id))

    @commands.command()
    async def listTemplateChannels(self, ctx):
        embed = discord.Embed(title = "Template Channels")
        nameslist = []
        for channelID in self.template_channel_IDs:
            channel = discord.utils.get(ctx.guild.channels, id=channelID)
            #Remove manually deleted template channels still in list
            if channel == None:
                self.template_channel_IDs.remove(channelID)
            else:
                nameslist.append(channel.name)

        nameslist = '\n'.join(nameslist) # Joining the list with newline as the delimiter
        if len(nameslist) == 0:
            embed.add_field(name="Template Channels List", value="No Channels")
        else:
            embed.add_field(name="Template Channels List", value=nameslist)
        await ctx.send(embed=embed)
        
               
            
        
