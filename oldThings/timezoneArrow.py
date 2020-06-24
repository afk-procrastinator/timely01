import googlemaps
from timezonefinder import TimezoneFinder
import discord
from discord.ext import commands
from discord.utils import get
import random
import time
import sys
from dateutil import tz
import datetime as dt
import pytz
import shlex
import arrow as ar
import asyncio
import threading
from threading import Thread

'''
embed = discord.Embed(title="⏲ Your reminder is here! ⏲", colour=discord.Colour(botColor))
embed.add_field(name = "Created at:", value = "Created on: " + str(timeCreated))
embed.add_field(name = "Message from your past self:", value = message)
channel = await user.create_dm()
await channel.send(embed = embed)
'''

month = ["months", "month", "mo", "mos"]
week = ["weeks", "week", "wk", "wks"]
day = ["days", "day", "dy", "dys"]
hour = ["hours", "hour", "hr", "hrs"]
min = ["minutes", "minute", "min", "mins"]

def difference(inFormat, difference):
    if inFormat in min:
        return difference * 60
    elif inFormat in hour:
        return difference * 3600
    elif inFormat in day:
        return difference * 86400
    elif inFormat in week:
        return difference * 604800
    elif inFormat in month:
        return difference * 2628000
threads = []
def timer(length, message):
    time.sleep(length)
    print("timer up! message:", message)

# syntax: remind USER "MESSAGE" TIME UNITS [def mins]
command = input("remind ")
command = shlex.split(command)
user = command[0]
message = command[1]
length = command[2]
units = command[3]
args = 0
length = len(command)
print(length)
i = 1
arguments = []
timeAdd = 0
remindString = ""
while i < (length-1):
    print("argument: ", command[i+1], command[i+2])
    remindString = remindString + " " + command[i+1] + command[i+2]
    additional = difference(command[i+2], int(command[i+1]))
    timeAdd += additional
    i += 2
print(remindString)
print(timeAdd)

threading.Thread(target = timer, args = [timeAdd, message]).start()

# OLD FUNCTIONS AND CODE
'''
# GOAL OF THIS FUNCTION: TAKE IN CURRENT DATE IN UTC (ADD SUPPORT FOR OTHER TZ WHEN IN BOT.PY), PARSE PLAIN LANGUAGE TO DATE, FIND AMOUNT OF TIME BETWEEN THEM.
# ALSO, CHOOSE IF RESPONSE IS IN YEARS, MONTHS, WEEKS, DAYS, HOURS, MINS, OR SECONDS!
# SEPERATE COMMAND FOR HOURS UNTIL/LESS TIME
now = ar.utcnow()
startDate = input("Time until: [DD/MM/YYYY]: ")
inFormat = input("What format? [Year, Month, Week, Day] ")
try:
    startDateParsed = ar.get(startDate, 'DD/MM/YYYY')
except ar.ParserError:
    print("error")
difference = startDateParsed - now
inFormat = inFormat.lower()
difference = difference.days
print(difference)
if inFormat in ["years", "year", "yr", "yrs"]:
    differenceQ = (divmod(difference, 365))
    differenceQ2 = (divmod(differenceQ[1], 30))
    differenceQ3 = (divmod(differenceQ2[1], 7))
    print("In years: ", differenceQ[0], "\nMonths:", differenceQ2[0], "\nWeeks:", differenceQ3[0], "\nDays:", differenceQ3[1])
elif inFormat in ["months", "month", "mo", "mos"]:
    differenceQ = (divmod(difference, 30))
    differenceQ2 = (divmod(differenceQ[1], 7))
    print("In months: ", differenceQ[0], "\nWeeks:", differenceQ[1], "\nDays:", differenceQ2[1])
elif inFormat in ["weeks", "week", "wk", "wks"]:
    differenceQ = (divmod(difference, 7))
    print("In weeks: ", differenceQ[0], "\nDays:", differenceQ[1])
elif inFormat in ["days", "day", "dy", "dys"]:
    differenceQ = (divmod(difference, 1))
    print("difference in days: ", differenceQ[1])
else: 
    print("error")
gmaps = googlemaps.Client(key="AIzaSyBaaZgL-vPzNjAKVrgCNZLqVMR8R05SeRU")
lat = 0
lon = 0
tf = TimezoneFinder()
time_start = time.time()
seconds = 10
minutes = 0
# function to return the progress bar ASCII
def progressBar(value, endvalue, bar_length=20):
        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        timeDelta = dt.timedelta(endvalue - value)
        print(timeDelta)
        sys.stdout.write("\rPercent: [{0}] {1}%, Time remaining: {2}".format(arrow + spaces, int(round(percent * 100)), timeDelta))
        sys.stdout.flush()
def countdown(init):
    t = 0
    while t < init + 1:
        progressBar(t, init)
        t += 1
        time.sleep(1)
    print("\nComplete!")
print("How many seconds to count down? Enter an integer:")
seconds = input()
while not seconds.isdigit():
    print("That wasn't an integer! Enter an integer:")
    seconds = input()
seconds = int(seconds)
countdown(seconds)
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
def timeZone(input):
    global lat, lon
    testing = gmaps.geocode(input)
    lat = extract_values(testing, "lat")[0]
    lon = extract_values(testing, "lng")[0]
    region = tf.timezone_at(lng=lon, lat=lat)
    utc = ar.utcnow()
    shifted = utc.to(region)
    formatted = shifted.format("HH:mm:ss")

    print("time in", input, "is:", formatted)
'''
