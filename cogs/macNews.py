import discord
from discord.ext import commands, tasks
from discord.ext.commands.errors import ChannelNotReadable
from discord.utils import get
from requests import get
from bs4 import BeautifulSoup


url = 'https://dailynews.mcmaster.ca/'

def getLatestArticle(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    article_containers = html_soup.find_all('div', class_ = 'article-in-archive grid-container section one-post-section has-social blog-id-') 
    most_recent_article = article_containers[0]

    imageContainer = most_recent_article.find_all('div', class_ = "image-background")[0]
    imageSRC = imageContainer["lazy-background-image"][5:-2]
    link = (most_recent_article.a)["href"]
    date = (most_recent_article.p.text).strip()
    title = (most_recent_article.h3.a)["title"]
    subtitle = most_recent_article.find_all('div', class_ = "large-6 large-offset-1 cell read-cell")[0].find_all('p')[1].a.text.strip()

    return [title,subtitle,date,link,imageSRC]

def makeEmbed(articleTitle,articleSubtitle,articleDate,articleLink,articleImageSRC):
    embed = discord.Embed(title= articleTitle, url=articleLink,
    description= articleSubtitle, color = 0xFF5733)
    embed.set_thumbnail(url=articleImageSRC)
    return embed


class macNews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.most_recent_article_url = ""
        self.channelIDs = [] 
        self.getNews.start()
    
    @tasks.loop(seconds = 3600)
    async def getNews(self):
        [articleTitle,articleSubtitle,articleDate,articleLink,articleImageSRC] = getLatestArticle(url)
        if articleLink == self.most_recent_article_url:
            #print("No New News article found")
            #print()
            return
        
        self.most_recent_article_url = articleLink
        embed = makeEmbed(articleTitle,articleSubtitle,articleDate,articleLink,articleImageSRC)
        
        for channelID in self.channelIDs:
            channel = await self.bot.fetch_channel(channelID)
            await channel.send(embed=embed)
        
 
    @commands.command()
    async def getNewsManually(self, ctx):
        [articleTitle,articleSubtitle,articleDate,articleLink,articleImageSRC] = getLatestArticle(url)
        embed =  makeEmbed(articleTitle,articleSubtitle,articleDate,articleLink,articleImageSRC)
        self.most_recent_article_url = articleLink
        for channelID in self.channelIDs:
            channel = await self.bot.fetch_channel(channelID)
            await channel.send(embed=embed)
    
    @commands.command()
    async def addNewsChannel(self, ctx, id):
        for channel in ctx.guild.channels:
            if id == str(channel.id) and channel.id not in self.channelIDs:
                self.channelIDs.append(channel.id)
                await ctx.send('Added Channel: "{channel}" to News Channel List'.format(channel=channel))
                return
        await ctx.send("Invalid channel ID or Duplicate. ")
    
    @commands.command()
    async def removeNewsChannel(self, ctx, id):
        for channel in ctx.guild.channels:
            if (id == str(channel.id)) and (channel.id in self.channelIDs):
                self.channelIDs.remove(int(id))
                await ctx.send("Removed Channel \"{channel}\" From News Channel List".format(channel=channel))
                return
        
        await ctx.send("Invalid ID. You sent {id}".format(id = id))

    @commands.command()
    async def listNewsChannels(self, ctx):
        embed = discord.Embed(title = "News Channels")
        nameslist = []
        for channelID in self.channelIDs:
            channel = discord.utils.get(ctx.guild.channels, id=channelID)
            #Remove manually deleted template channels still in list
            if channel == None:
                self.channelIDs.remove(channelID)
            else:
                nameslist.append(channel.name)

        nameslist = '\n'.join(nameslist) # Joining the list with newline as the delimiter
        if len(nameslist) == 0:
            embed.add_field(name="News Channels List", value="No Channels")
        else:
            embed.add_field(name="News Channels List", value=nameslist)
        await ctx.send(embed=embed)
