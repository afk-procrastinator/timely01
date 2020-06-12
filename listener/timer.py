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
import asyncio
import json


commandKey = '?'
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
bot = commands.Bot(command_prefix=commandKey)
tf = TimezoneFinder()
lat = 0
botColor = 0x176BD3
lon = 0
region = ""
timeVibeRole = False
cancelTimer = False


month = ["months", "month", "mo", "mos"]
week = ["weeks", "week", "wk", "wks"]
day = ["days", "day", "dy", "dys"]
hour = ["hours", "hour", "hr", "hrs"]
min = ["minutes", "minute", "min", "mins"]

class TimerListener(commands.Cog):
    
    @bot.command()
    async def timer(self, ctx, arg1: int, arg2: str):
        units = ""
        possibleCommands = ["seconds", "sec", "secs", "s", "minutes", "hours", "minute", "hour", "m", "mins", "hr", "hrs"]
        if arg2 in possibleCommands:
            units = arg2
        else:
            embed = discord.Embed(title="Timer error:", colour=discord.Colour(botColor))
            embed.add_field(name="Syntax error", value="Whoops! Syntax error. Command should be: \n ```?timer length unit``` \n Units can only be `hours`, `minutes`, or `seconds`. Please use the `?reminder` command for anything longer.")
            await ctx.send(embed = embed)
            return
        if arg2 in ["minutes", "minute", "m", "mins"]:
            arg1 = arg1 * 60
            print("mins")
        elif arg2 in ["hours", "hour", "hr", "hrs"]:
            arg1 = arg1 * 3600
            print("hrs")
        totalTime = time.strftime("%H:%M:%S", time.gmtime(arg1))
        if arg1 > 43200:
            embed = discord.Embed(title="Timer too long!", colour=discord.Colour(botColor))
            embed.add_field(name="Progress Bar", value="Your timer is over 12 hours! Why don't you try the `?reminder` command instead?")
            await ctx.send(embed=embed)
            return
        t = 0
        while t < arg1 + 1:
            bar_length = 20
            percent = float(t) / arg1
            arrow = '-' * int(round(percent * bar_length)-1) + '>'
            spaces = ' ' * (bar_length - len(arrow))
            timeRemaining = time.strftime("%H:%M:%S", time.gmtime(int(arg1-t)))
            string = ("```\rPercent: [{0}] {1}%```".format(arrow + spaces, int(round(percent * 100))))
            embed = discord.Embed(title="⏱: {0}".format(timeRemaining), colour=discord.Colour(botColor))
            embed.add_field(name="⏳", value=string)
            if t == 0:
                message = await ctx.send(embed=embed)
            else:
                await message.edit(embed=embed)
            t += 1
            await asyncio.sleep(1)
            if cancelTimer == True:
                print("cancelled")
                string = ("_**CANCELLED_**")
                embed = discord.Embed(title="⏱", colour=discord.Colour(botColor))
                embed.add_field(name="⏱", value=string)
                return
        string = ("_**FINISHED**_")
        embed = discord.Embed(title="💫🎉🎉🎉💫", colour=discord.Colour(botColor))
        embed.add_field(name="💫🎉🎉🎉💫", value=string)
        await message.edit(embed=embed)

    @bot.command()
    async def cancel(self, ctx):
        global cancelTimer
        cancelTimer == True
        print("true")
    # error with the timer command 
    @timer.error
    async def timer_error(self, ctx, error):
        print(error)

    

def setup(client):
    client.add_cog(TimerListener(client))
    print('TimerListener is Loaded')   