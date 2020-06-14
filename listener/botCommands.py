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

data_folder = Path("files/")

commandKey = 't!'
token = settings.TOKEN
bot = commands.Bot(command_prefix=commandKey)
botColor = 0x176BD3


class botCommandsListener(commands.Cog):

    @bot.command() #NON OPERATIONAL RN 
    async def status(self, ctx, *args):
        game = discord.Game(args)
        await ctx.change_presence(self, status=bot.status.idle, activity=game)
        

  
def setup(client):
    client.add_cog(botCommandsListener(client))
    print('botCommandsListener is Loaded') 