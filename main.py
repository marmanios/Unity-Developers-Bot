import discord
import os

from dotenv import load_dotenv

from tempVoice.tempVoice import tempVoice
from Music.music import Music


intents = discord.Intents.default()
intents.members = True
client = discord.ext.commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Bussin"))
  print("ready")

client.add_cog(tempVoice(client, 669400622038253568))
client.add_cog(Music(client))

@client.command()
async def restartMusic(ctx):
  client.remove_cog(Music(client))
  client.add_cog(Music(client))

load_dotenv()

client.run(os.getenv('BOT_TOKEN'))