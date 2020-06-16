import googlemaps
from timezonefinder import TimezoneFinder
import discord
from discord.ext import commands
from discord.utils import get
from dateutil import tz 
import arrow as ar
import datetime as dt
from dotenv import load_dotenv
import os
import settings
import time
import sys
import csv
import asyncio
import json
from pathlib import Path


def get_prefix(client, message):
    with open('files/prefix.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

data_folder = Path("files/")

token = settings.TOKEN
bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command("help")
botColor = 0x176BD3

helpString = """
**Timezone Calculator: ** *Gives you current time and date in a location*
`{}tz` `location`
**e.g.** `{}tz new york`

**Currency Calculator: ** *Converts an amount of money between two currencies*
`{}convert` `value` `currency` `to` `currency`
**e.g.** `{}convert 10 usd to eur`

**Time Distance: ** *Calculates the number of days/weeks/months/years between today and a date*
`{}dis` `date: [DD/MM/YYYY]` `time units [days, weeks, months, years]`
**e.g.** `{}dis 30/08/2021 weeks`

**Reminder & Timer: ** 
`{}remind` `@user` `message` `amount of time` *Reminds you of a message after a certain amount of time by sending you a DM*
**e.g.** `{}remind @TimeVibe "go to sleep" 20 mins`

`{}timer` `amount` `units` *Shows a timer in chat! Good for short times (> 1 hour)
**e.g.** `{}timer 10 seconds`

**Fun stuff:**
`{}movie` `title` *Gives IMDB data on a movie*
**e.g.** `{}movie blade runnner`

`{}friendship` *Sends you a DM to access commands in your messages*

`{}hltb` `title` *Returns information on how long to beat a given videogame. Data from HLTB.*
"""

    
class botCommandsListener(commands.Cog):

    @bot.command()
    async def help(self, ctx):
        prefix = get_prefix(bot, ctx.message)
        embed = discord.Embed(title="Help is here!", colour=discord.Colour(botColor))
        embed.add_field(name=" __**Command Categories:**__", value=helpString.format(prefix))
        await ctx.send(embed=embed)

    @bot.command() #NON OPERATIONAL RN 
    async def status(self, ctx, *args):
        game = discord.Game(args)
        await ctx.change_presence(self, status=bot.status.idle, activity=game)
        
    @bot.command()
    async def friendship(self, ctx):
        user = ctx.message.author
        embed = discord.Embed(title="Wanna be friends?", colour=discord.Colour(botColor))
        embed.add_field(name="<3 <3 <3", value="Just slid into your DMs! Now you can access commands from the comfort of your messages.")
        await user.send(embed=embed)

        
        
def setup(client):
    client.add_cog(botCommandsListener(client))
    print('botCommandsListener is Loaded') 