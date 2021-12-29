import discord
from discord.ext import commands
from discord.utils import get

emojis = {
  "♂️":925251325585932288,
  "♀️":925251382871752754,
  "🎮":925251408649916427,
  "🔊":925251444196663337,
  "🖌️":925251492791873576,
  "🕸️":925251564686413866,
}

rolls_channel_id = None

class giveRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        global polls_msg
        if (reaction.message.id != polls_msg.id):
            return
        
        if (reaction.emoji in emojis):
            Role = get(reaction.message.guild.roles, id = emojis[reaction.emoji])
            await user.add_roles(Role)

        else:
            await reaction.message.remove_reaction(reaction.emoji, user)
    
    @commands.command()
    async def createRollPoll(self, ctx):
        global polls_msg
        polls_msg = await ctx.send("EMBED")
