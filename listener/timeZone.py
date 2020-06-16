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
import re

from master import get_prefix
bot = commands.Bot(command_prefix=get_prefix)
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
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

def getRegion(self, input):
    utc = ar.utcnow()
    shifted, region = timeZone(self, input)
    shifted = utc.to(region)
    formatted = shifted.format("HH:mm:ss")
    region = region.split("/")[1].replace("_", " ")
    return region, formatted

class TimeListener(commands.Cog):
    
    @bot.command()
    async def tzset(self, ctx, input: str):
        region, formatted = getRegion(self, input)
        user = ctx.message.author
        with open('files/{}.json'.format(ctx.guild.id), 'r+') as file:
                addData = {str(user.id): region}
                data = json.load(file)
                data.update(addData)
                file.seek(0)
                json.dump(data, file)
        embed = discord.Embed(title="**Timezone set!**", colour=discord.Colour(botColor))
        embed.add_field(name="🌍🌍🌍", value= "Timezone for <@{0}> is set to {1}".format(ctx.message.author.id, region))
        await ctx.send(embed=embed)

    # tz command: takes one arg, gives time at location
    @bot.command()
    async def tz(self, ctx, input):
        prefix = get_prefix(bot, ctx.message)
        if input.startswith("<"):
            string = re.sub("<|>|@|!", "", input)
            print(string)
            with open('files/{}.json'.format(ctx.guild.id), 'r') as file:
                data = json.load(file)
                if string in data:
                    input = data[string]
                else:
                    embed = discord.Embed(title="**Timezone not set**", colour=discord.Colour(botColor))
                    embed.add_field(name="🌍🌍🌍" , value= "User {0} has not set a region! Use `{1}tzset location` to set!".format(input, prefix))
                    await ctx.send(embed=embed)
        region, formatted = getRegion(self, input)
        embed = discord.Embed(title="**Timezone**", colour=discord.Colour(botColor))
        embed.add_field(name="Local time in: **" + region + "**", value= formatted)
        await ctx.send(embed=embed)
                
    @tz.error
    async def tz_error(self, ctx, error):
        embed = discord.Embed(title="**Timezone Error**", colour = discord.Color(botColor))
        prefix = get_prefix(bot, ctx.message)
        embed.add_field(name = "_**Please try again!**_", value = "Your query returned no significant data. Please try again! \n \nExample: `{0}tz moscow`".format(prefix))
        message = await ctx.send(embed = embed)
        await asyncio.sleep(2)
        await message.delete()

def setup(client):
    client.add_cog(TimeListener(client))
    print('TimeListener is Loaded') 