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
sendDict = {} # NOT IN USE RN 

resetLoop = False

async def sendDM(input):
    timeAdd = input["timeAdd"]
    user = input["user"]
    timeCreated = input["timeCreated"]
    message = input["message"]
    guild = input["guild"]
    print(userSend)
    channel = await userSend.create_dm()
    
    embed = discord.Embed(title="⏲ Your reminder is here! ⏲", colour=discord.Colour(botColor))
    embed.add_field(name = "The reminder was set at:", value = timeCreated )
    embed.add_field(name = "Your message is:", value = message)
    await channel.send(embed = embed)

async def append(length: str, input: dict):
    toOpen = data_folder / length
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
    global loopDict
    global resetLoop
    length = len(loopDict)
    print(length)
    if length == 0:
        task = asyncio.create_task(runLoop())
        taskShort = asyncio.create_task(runShort(self))
        resetLoop = False
        loopDict[str(length)] = (input)
    else: 
        resetLoop = True
        loopDict[str(length)] = (input)
        resetLoop = False

# Takes dict and figures out where it belongs 
async def runAppend(self, importDict: dict):
    timeAdd = importDict["timeAdd"]
    guild = importDict["guild"]
    guildStringLong = "long.csv"
    guildStringShort = "short.csv"
    if timeAdd > 60 and timeAdd < 1440 : # over a hour from now but less than an 24 hours -- short
        await append(guildStringShort, importDict)
    elif timeAdd >= 1440: # over a day from now
        await append(guildStringLong, importDict)
    elif timeAdd <= 61: # less than an hour than now -- loop dict THIS IS WHERE WORK IS NEEDED 
        await addToLoop(self, importDict)

async def runShort(self):
    while True:
        print("repeat")
        with open('files/short.csv', newline='', mode = 'r') as csvfile:
            dict_list = []
            reader = csv.DictReader(csvfile)
            for line in reader:
                line["timeAdd"] = int(line["timeAdd"]) - 1
                print(line)
                #dict_list[]
        
        os.remove("files/short.csv")
        with open('files/short.csv', newline='', mode = 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
            writer.writeheader()
            writer.writerows(dict_list)
        
        await asyncio.sleep(1)
 
    
async def runLoop():
    global resetLoop
    global loopDict
    while True:
        if resetLoop == False:
            print("running")
            print(loopDict)
            for key in loopDict:
                print(loopDict[key]["timeAdd"])
                loopDict[key]["timeAdd"] -= 1
                if loopDict[key]["timeAdd"] == 0:
                    await sendDM(loopDict[key])
                    del loopDict[key]
                print(loopDict[key]["timeAdd"])
        elif resetLoop == True:
            print("stopping")
            break
        await asyncio.sleep(1)

# Formats various lengths to minutes
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

class ReminderListener(commands.Cog):

    @bot.command()
    async def test(self, ctx):
        await runShort(self)

    @bot.command()
    async def remind(self, ctx, user: discord.Member, message: str, *arg):
        global ctxG
        global userSend
        userSend = user
        ctxG = ctx
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
            timeAdd += additional
            i += 2
        dictToSend = dict({"timeAdd": timeAdd, "user": user.id, "timeCreated": timeCreated, "message": message, "guild": ctx.guild.id})
        await runAppend(self, dictToSend)
        embed = discord.Embed(title="⏲ Your reminder is set! ⏲", colour=discord.Colour(botColor))
        embed.add_field(name = "You will be reminded in:", value = str(timeAdd) + " minutes")
        embed.add_field(name = "Your message is:", value = message)
        await ctx.send(embed = embed)

    @remind.error
    async def remind_error(self, ctx, error):
        if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Syntax error >:(", colour = discord.Colour(botColor))
            embed.add_field(name = "Correct syntax:", value = "`?remind @user \"message\" time`\ne.g. `?remind @TimeVibe \"Your message here\" 1 week 10 hours 3 minutes`")
            await ctx.send(embed = embed)


'''
Every minute run a function that loops through loopDict
    Check if resetLoop == true, in which case append sendDict to loopDict
        Iterate through loopDict, add each one to sendDict
        A check to make sure the reminder time hasn't already passed
'''
        
def setup(client):
    client.add_cog(ReminderListener(client))
    print('ReminderListener is Loaded') 