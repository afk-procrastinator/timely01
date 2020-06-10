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


loopDict = {}

def append(guild: str, input: dict):
        if os.path.isfile(guild):
            print ("File exists and is readable")   
            with open(guild, 'a') as f:
                json.dump(input, f)
        else:
            print ("Either file is missing or is not readable, creating file...")
            file = open(guild,"a")
            with open(guild, 'a') as f:
                    json.dump(input, f)


def runAppend(importDict: dict):
    timeAdd = importDict["timeAdd"]
    user = importDict["user"]
    timeCreated = importDict["timeCreated"]
    message = importDict["message"]
    guild = importDict["guild"]
    guildStringLong = str(guild) + "long.json"
    guildStringShort = str(guild) + "short.json"
    append(guildStringLong, importDict)
    if timeAdd <= 60:
        


# min in hour: 60
# min in 24 hours: 1140