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

commandKey = '?'
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
bot = commands.Bot(command_prefix=commandKey)
botColor = 0x176BD3


month = ["months", "month", "mo", "mos"]
week = ["weeks", "week", "wk", "wks"]
day = ["days", "day", "dy", "dys"]
hour = ["hours", "hour", "hr", "hrs"]
min = ["minutes", "minute", "min", "mins"]
csv_columns = ["timeAdd", "user", "timeCreated", "message", "guild"]
loopDict = {}
sendDict = {}


async def append(guild: str, input: dict):
    toOpen = data_folder / guild
    if os.path.isfile(toOpen):
        print ("File exists and is readable")   
        try:
            with open(toOpen, "a") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
                writer.writerow(input)
        except IOError:
            print("error")
    else:
        print ("Either file is missing or is not readable, creating file...")
        try:
            with open(toOpen, "w") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
                writer.writeheader()
                writer.writerow(input)
        except IOError:
            print("error")

async def addToLoop(self, input: dict):
    length = len(loopDict)
    loopDict[str(length)] = input 
    #print(loopDict)
    
async def runAppend(self, importDict: dict):
    global sendDict
    timeAdd = importDict["timeAdd"]
    guild = importDict["guild"]
    guildStringLong = str(guild) + "long.csv"
    guildStringShort = str(guild) + "short.csv"
    if timeAdd > 60 and timeAdd < 1440 : # over a hour from now but less than an 24 hours -- short
        await append(guildStringShort, importDict)
    elif timeAdd >= 1440: # over a day from now
        await append(guildStringLong, importDict)
    elif timeAdd <= 30: # less than an hour than now -- loop dict
        addToLoop(importDict)
        sendDict = importDict

def formatToMin(self, inFormat, difference):
        if inFormat in min:
            return difference
        elif inFormat in hour:
            return difference * 60
        elif inFormat in day:
            return difference * 1440
        elif inFormat in week:
            return difference * 10080
        elif inFormat in month:
            return difference * 43800

async def createFile(self, ctx, append):
    guildID = (ctx.guild.id)
    greater24 = guildID + "greater"
    less24 = guildID + "less"


class ReminderListener(commands.Cog):

    @bot.command()
    async def remind(self, ctx, user: discord.Member, message: str, *arg):
        command = []
        for args in arg: 
            command.append(args)
        args = 0
        length = len(command)
        print(command)
        i = 0
        arguments = []
        timeAdd = 0
        timeNow = ar.utcnow()
        timeCreated = timeNow.format("MMMM Do, YYYY [at] DD:mm")
        while i < (length - 1):
            print("argument: ", command[i], command[i+1])
            additional = formatToMin(self, command[i+1], int(command[i]))
            print(additional)
            timeAdd += additional
            print(timeAdd)
            i += 2
        dictToSend = dict({"timeAdd": timeAdd, "user": user.id, "timeCreated": timeCreated, "message": message, "guild": ctx.guild.id})
        await runAppend(self, dictToSend)
        embed = discord.Embed(title="⏲ Your reminder is set! ⏲", colour=discord.Colour(botColor))
        embed.add_field(name = "You will be reminded in:", value = str(timeAdd) + " minutes")
        embed.add_field(name = "Your message is:", value = message)
        await ctx.send(embed = embed)
'''
    @remind.error
    async def remind_error(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Syntax error >:(", colour = discord.Colour(botColor))
            embed.add_field(name = "Correct syntax:", value = "`?remind @user \"message\" time`\ne.g. `?remind @TimeVibe \"Your message here\" 1 week 10 hours 3 minutes`")
            await ctx.send(embed = embed)
'''
    
    
    
    
def setup(client):
    client.add_cog(ReminderListener(client))
    print('ReminderListener is Loaded') 