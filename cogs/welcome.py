import discord
from discord.ext import commands, tasks
from discord.ext.commands.errors import ChannelNotReadable
from discord.utils import get

class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.serverWelcomeMessages = {}
 
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("JOINED")
        if member.id == 202255919965274112:
            await member.add_roles(get(member.guild.roles, id = 925341644394479637))
            embed = self.serverWelcomeMessages[member.guild]
            dm_channel = await member.create_dm()
            if embed == None:
                await dm_channel.send("No Server Welcome Message Setup")
            else:
                await dm_channel.send(embed = embed)
    
    @commands.command()
    async def setWelcomeMessage(self, ctx, *,message):
        embedTitle = "Welcome To " + ctx.guild.name
        embed = discord.Embed(title= embedTitle, description= message , color = 0xFF5733)
        embed.set_thumbnail(url=ctx.guild.icon)
        self.serverWelcomeMessages[ctx.guild] = embed
        await ctx.send("Welcome Message set to \"{message}\"".format(message = message))
    


   