import discord
from discord.ext import commands
from discord.utils import get
from cogs.giveRoles import giveRoles
from cogs.tempVoice import tempVoice
from cogs.macNews import macNews
from cogs.welcome import welcome

TOKEN = "OTI1MjQ4NDgxNTU0MjAyNjM0.YcqWzA.tE3fxihTC-rVIZPBTe0R0V9pgBU"
client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  print("ready")

client.add_cog(giveRoles(client))
client.add_cog(macNews(client))
client.add_cog(tempVoice(client))
client.add_cog(welcome(client))

@client.command()
async def Help(ctx):
  embed = discord.Embed(title= "McMaster Unity Developers", url="https://google.com",
  description= "Insert description here", color = 0xFF5733)

  embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/925241975886712852/925258137752195112/Unity_2021.svg.png")

  await ctx.send(embed=embed)

client.run(TOKEN)