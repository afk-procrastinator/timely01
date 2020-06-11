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
import io
import json
import threading
import csv

commandKey = '?'
bot = commands.Bot(command_prefix=commandKey)
csv_columns = ["timeAdd", "user", "timeCreated", "message", "guild"]
loopDict = {}
sendDict = {}

def append(guild: str, input: dict):
        if os.path.isfile(guild):
            print ("File exists and is readable")   
            try:
                with open(guild, "a") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
                    writer.writerow(input)
            except IOError:
                print("error")
        else:
            print ("Either file is missing or is not readable, creating file...")
            try:
                with open(guild, "w") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
                    writer.writeheader()
                    writer.writerow(input)
            except IOError:
                print("error")


def addToLoop(input: dict):
    length = len(loopDict)
    loopDict[str(length)] = input 
    #print(loopDict)
    
async def runAppend(importDict: dict):
    global sendDict
    timeAdd = importDict["timeAdd"]
    guild = importDict["guild"]
    guildStringLong = str(guild) + "long.csv"
    guildStringShort = str(guild) + "short.csv"
    if timeAdd > 60 and timeAdd < 1440 : # over a hour from now but less than an 24 hours -- short
        append(guildStringShort, importDict)
    elif timeAdd >= 1440: # over a day from now
        append(guildStringLong, importDict)
    elif timeAdd <= 30: # less than an hour than now -- loop dict
        addToLoop(importDict)
        sendDict = importDict
        await sendReminder()
    
@bot.listen()
async def sendReminder():
    print("sendDict")
    
        


# min in hour: 60
# min in 24 hours: 1140