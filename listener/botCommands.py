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
import requests
import re
import json
from pathlib import Path
from master import get_prefix
from master import get_color

data_folder = Path("files/")

token = settings.TOKEN
bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command("help")

helpString1 = """
**Timezone Calculator: ** *Gives you current time and date in a location*
`{0}tz` `location`
**e.g.** `{0}tz new york`

**Currency Calculator: ** *Converts an amount of money between two currencies*
`{0}convert` `value` `currency` `to` `currency`
**e.g.** `{0}convert 10 usd to eur`

**Time Distance: ** *Calculates the number of days/weeks/months/years between today and a date*
`{0}dis` `date: [DD/MM/YYYY]` `time units [days, weeks, months, years]`
**e.g.** `{0}dis 30/08/2021 weeks`

**Reminder & Timer: ** 
`{0}remind` `@user` `message` `amount of time` *Reminds you of a message after a certain amount of time by sending you a DM*
**e.g.** `{0}remind @TimeVibe "go to sleep" 20 mins`

`{0}timer` `amount` `units` *Shows a timer in chat! Good for short times (> 1 hour)
**e.g.** `{0}timer 10 seconds`

"""

helpString2 = """**Fun stuff:**
`{0}movie` `title` *Gives IMDB data on a movie*
**e.g.** `{0}movie blade runnner`

`{0}friendship` *Sends you a DM to access commands in your messages*

`{0}hltb` `title` *Returns information on how long to beat a given videogame. Data from HLTB.*
"""
class botCommandsListener(commands.Cog):

    @bot.command()
    async def help(self, ctx):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Help is here!", colour=color)
        embed.add_field(name=" __**Command Categories:**__", value=helpString1.format(prefix))
        embed.add_field(name=" __**Command Categories:**__", value=helpString2.format(prefix))
        await ctx.send(embed=embed)
        
    @bot.command()
    async def friendship(self, ctx):
        user = ctx.message.author
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Wanna be friends?", colour=discord.Colour(color))
        embed.add_field(name="<3 <3 <3", value="Just slid into your DMs! Now you can access commands from the comfort of your messages.")
        await user.send(embed=embed)

    @bot.command()
    async def prefix(self, ctx, prefix):
        with open('files/{}.json'.format(ctx.guild.id), 'r') as f:
            prefixes = json.load(f)    
        prefixes["info"]["prefix"] = prefix
        with open('files/{}.json'.format(ctx.guild.id), 'w' ) as f:
            json.dump(prefixes, f, indent = 4)

    @bot.command()
    async def color(self, ctx):
       with open('files/{}.json'.format(ctx.guild.id), 'r') as f:
           color = json.load(f)   
       hexa = color["info"]["color"]
       prefix = get_prefix(bot, ctx.message)
       hex_str = hexa
       hex_int = int(hex_str, 16)
       new_int = hex_int + 0x200
       hexa = hexa.replace("0x", "")
       if new_int > 16777215:
           new_int = 16777214
       url = "http://www.thecolorapi.com/id?hex={}".format(hexa)
       response = requests.get(url)
       data = json.loads(response.text)
       image = (data["image"]["named"])
       embed = discord.Embed(title="Color settings!", colour=new_int)
       embed.add_field(name="Your current color:", value="**#{0}**\nSet a new color with `{1}colorset HEX`".format(hex_str.replace("0x",""), prefix))
       embed.set_thumbnail(url="http://www.singlecolorimage.com/get/{}/100x100".format(hexa))
       await ctx.send(embed=embed)
    
    @bot.command()
    async def colorset(self, ctx, hex):
        hex = hex.replace("#", "")
        match = re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', hex)
        if match:
            with open('files/{}.json'.format(ctx.guild.id), 'r') as f:
                color = json.load(f)    
            color["info"]["color"] = "0x"+hex
            with open('files/{}.json'.format(ctx.guild.id), 'w' ) as f:
                json.dump(color, f, indent = 4)
        else:
            color = int(get_color(bot, ctx.message))
            embed = discord.Embed(title="Error:", colour=discord.Colour(color))
            embed.add_field(name="Not a valid hex code!", value="Please try again!")
            message = await ctx.send(embed = embed)
            await asyncio.sleep(2)
            await message.delete()

        
        
def setup(client):
    client.add_cog(botCommandsListener(client))
    print('botCommandsListener is Loaded') 