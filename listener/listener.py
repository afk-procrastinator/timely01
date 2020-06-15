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
import csv
import json
import threading
from threading import Thread
import numba.cuda.tests.cudadrv.test_detect

from master import get_prefix
bot = commands.Bot(command_prefix=get_prefix)
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
tf = TimezoneFinder()
lat = 0
botColor = 0x176BD3
lon = 0
region = ""
timeVibeRole = False
cancelTimer = False

threads = []

month = ["months", "month", "mo", "mos"]
week = ["weeks", "week", "wk", "wks"]
day = ["days", "day", "dy", "dys"]
hour = ["hours", "hour", "hr", "hrs"]
min = ["minutes", "minute", "min", "mins"]

csv_columns = ["timeAdd", "user", "timeCreated", "message", "guild"]
loopDict = {}
sendDict = {}

class GeneralListener(commands.Cog):
    
    # only allows Admin to call the setup()
    @bot.command()
    async def setup(self, ctx, input: str, *args: str):
        if input == "role":
            print("role")
            guild = ctx.guild
            selfRole = guild.roles
            for role in selfRole:
                if role == "TimeVibeRole":
                    print(role.id)
                    timeVibeRole = True
                    await ctx.send("Bot role already exists!")
        if timeVibeRole == False:
            print("create")
            role = guild.create_role(name="TimeVibeRole")
            await role
            await bot.add_roles(bot, role)       
    # setup command error handling
    @setup.error
    async def setup_error(self, ctx, error):
       if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="**Argument error**", colour=discord.Colour(botColor))
        embed.add_field(name="Possible arguments:", value="`role` - creates role for bot, only needed for initialization.")
        await ctx.send(embed=embed)
    
def setup(client):
    client.add_cog(GeneralListener(client))
    print('GeneralListener is Loaded')   