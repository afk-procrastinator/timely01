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

commandKey = 't!'
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
bot = commands.Bot(command_prefix=commandKey)
tf = TimezoneFinder()
lat = 0
botColor = 0x176BD3
lon = 0
region = ""

# Extracts all key values from a dictionary obj
def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []
    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr
    results = extract(obj, arr, key)
    return results

def timeZone(self, input):
    global lat, lon
    utc = ar.utcnow()
    testing = gmaps.geocode(input)
    lat = extract_values(testing, "lat")[0]
    lon = extract_values(testing, "lng")[0]
    region = tf.timezone_at(lng=lon, lat=lat)
    shifted = utc.to(region)
    return shifted, region

class TimeListener(commands.Cog):
    # tz command: takes one arg, gives time at location
    @bot.command()
    async def tz(self, ctx, input: str):
        utc = ar.utcnow()
        shifted, region = timeZone(self, input)
        shifted = utc.to(region)
        formatted = shifted.format("HH:mm:ss")
        print(formatted)
        region = region.split("/")[1].replace("_", " ")
        embed = discord.Embed(title="**Timezone**", colour=discord.Colour(botColor))
        embed.add_field(name="Local time in: **" + region + "**", value= formatted)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(TimeListener(client))
    print('TimeListener is Loaded') 