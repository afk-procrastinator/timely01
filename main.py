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
import threading
from threading import Thread

from second import runAppend

commandKey = '?'
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
botColor = 0x176BD3
bot = commands.Bot(command_prefix=commandKey)
tf = TimezoneFinder()
lat = 0
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

def formatToMin(inFormat, difference):
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

async def createFile(ctx, append):
    guildID = (ctx.guild.id)
    greater24 = guildID + "greater"
    less24 = guildID + "less"


@bot.command()
async def remind(ctx, user: discord.Member, message: str, *arg):
    command = []
    for args in arg: 
        command.append(args)
    args = 0
    length = len(command)
    print(length)
    i = 0
    arguments = []
    timeAdd = 0
    timeNow = ar.utcnow()
    timeCreated = timeNow.format("MMMM Do, YYYY [at] DD:mm")
    while i < (length - 1):
        print("argument: ", command[i], command[i+1])
        additional = formatToMin(command[i+1], int(command[i]))
        print(additional)
        timeAdd += additional
        print(timeAdd)
        i += 2
    dictToSend = dict({"timeAdd": timeAdd, "user": user.id, "timeCreated": timeCreated, "message": message, "guild": ctx.guild.id})
    runAppend(dictToSend)
    embed = discord.Embed(title="⏲ Your reminder is set! ⏲", colour=discord.Colour(botColor))
    embed.add_field(name = "You will be reminded in:", value = timeAdd)
    embed.add_field(name = "Your message is:", value = message)
    await ctx.send(embed = embed)
    await time.sleep(timeAdd)

@remind.error
async def remind_error(ctx, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Syntax error >:(", colour = discord.Colour(botColor))
        embed.add_field(name = "Correct syntax:", value = "`?remind @user \"message\" time`\ne.g. `?remind @TimeVibe \"Your message here\" 1 week 10 hours 3 minutes`")
        await ctx.send(embed = embed)

# returns a progress bar with current value, end value, and length (customizable(?))
def progressBar(value, endvalue, bar_length=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length)-1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    timeDelta = dt.timedelta(endvalue - value)
    return ("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
# timer command. arg1 is the duration (up to 24 hours), arg2 is the units (seconds, minutes, hours)
# anything longer- several days, for instance, will be the ?reminder command
@bot.command()
async def timer(ctx, arg1: int, arg2: str):
    units = ""
    possibleCommands = ["seconds", "sec", "secs", "s", "minutes", "hours", "minute", "hour", "m", "mins", "hr", "hrs"]
    global cancelTimer
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
async def cancel(ctx):
    global cancelTimer
    cancelTimer == True
    print("true")
# error with the timer command 
@timer.error
async def timer_error(ctx, error):
    print(error)
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
    utc = ar.utcnow()
    testing = gmaps.geocode(input)
    lat = extract_values(testing, "lat")[0]
    lon = extract_values(testing, "lng")[0]
    region = tf.timezone_at(lng=lon, lat=lat)
    shifted = utc.to(region)
    return shifted, region
# tz command: takes one arg, gives time at location
@bot.command()
async def tz(ctx, input: str):
    utc = ar.utcnow()
    shifted, region = timeZone(input)
    shifted = utc.to(region)
    formatted = shifted.format("HH:mm:ss")
    region = region.split("/")[1].replace("_", " ")
    embed = discord.Embed(title="**Timezone**", colour=discord.Colour(botColor))
    embed.add_field(name="Local time in:", value=region)
    await ctx.send(embed=embed)
# tz error command handling
@tz.error
async def tz_error(ctx, error):
    print(error)
# only allows Admin to call the setup()
@bot.command()
async def setup(ctx, input: str, *args: str):
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
async def setup_error(ctx, error):
   if isinstance(error, commands.MissingRequiredArgument):
    embed = discord.Embed(title="**Argument error**", colour=discord.Colour(botColor))
    embed.add_field(name="Possible arguments:", value="`role` - creates role for bot, only needed for initialization.")
    await ctx.send(embed=embed)
# difference algorithm
def difference(initial: str, method: str):
    now = ar.utcnow()
    difference = initial - now
    inFormat = method.lower()
    difference = difference.days
    if inFormat in ["years", "year", "yr", "yrs"]:
        differenceQ = (divmod(difference, 365))
        if differenceQ[0] == 1:
            year = "year"
        else:
            year = "years"
        differenceQ2 = (divmod(differenceQ[1], 30))
        if differenceQ2[0] == 1:
            month = "month"
        else: 
            month = "months"
        differenceQ3 = (divmod(differenceQ2[1], 7))
        if differenceQ3[0] == 1:
            week = "week"
        else: 
            week = "weeks"
        if differenceQ3[1] == 1:
            day = "day"
        else:
            day = "days"
        string = "Time until: {0}: \n{1} {2}, {3} {4}, {5} {6}, and {7} {8}".format(initial.format("MMMM DD, YYYY"), str(differenceQ[0]), year, str(differenceQ2[0]), month,str(differenceQ3[0]) , week, str(differenceQ3[1], day))
        return string, initial.format("MMMM DD, YYYY:")
    elif inFormat in ["months", "month", "mo", "mos"]:
        differenceQ = (divmod(difference, 30))
        differenceQ2 = (divmod(differenceQ[1], 7))
        if differenceQ[0] == 1:
            month = "month"
        else: 
            month = "months"
        differenceQ3 = (divmod(differenceQ2[1], 7))
        if differenceQ2[0] == 1:
            week = "week"
        else: 
            week = "weeks"
        if differenceQ2[1] == 1:
            day = "day"
        else:
            day = "days"
        string = "Time until: {0}: \n{1} {2}, {3} {4}, {5} {6}".format(initial.format("MMMM DD, YYYY"), str(differenceQ[0]), month, str(differenceQ2[0]), week, str(differenceQ2[1]), day)
        return string, initial.format("MMMM DD, YYYY:")
    elif inFormat in ["weeks", "week", "wk", "wks"]:
        differenceQ = (divmod(difference, 7))
        if differenceQ[0] == 1:
            week = "week"
        else: 
            week = "weeks"
        if differenceQ[1] == 1:
            day = "day"
        else:
            day = "days"
        string = "Time until" + initial.format("MMMM DD, YYYY: \n") + str(differenceQ[0]) + " weeks and " + str(differenceQ[1]) + " days."
        string = "Time until: {0}: \n{1} {2}, {3} {4}".format(initial.format("MMMM DD, YYYY"), str(differenceQ[0]), week, str(differenceQ[1]), day)
        return string, initial.format("MMMM DD, YYYY:")
    elif inFormat in ["days", "day", "dy", "dys"]:
        differenceQ = (divmod(difference, 1))
        string = "Time until: "+ initial.format("MMMM DD, YYYY: \n") + str(differenceQ[0]) + " days."
        return string, initial.format("MMMM DD, YYYY:")
    else: 
        print("error")
# difference command
@bot.command()
async def dis(ctx, arg1:str, arg2:str):
    now = ar.utcnow()
    try:
        startDateParsed = ar.get(arg1, 'DD/MM/YYYY')
    except ar.ParserError:
        print("error")
    string, date = difference(startDateParsed, arg2)
    embed = discord.Embed(title="Days until: {0}".format(date), colour=discord.Colour(botColor))
    embed.add_field(name="⏰", value=string)
    await ctx.send(embed = embed)

    
# On bot login, send info
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="a game"))

# TESTING AND REFERENCE FUNCTIONS, WILL BE REMOVED BEFORE RELEASE

# Command to delete certain roles: FOR TESTING ONLY
@bot.command(pass_context=True)
async def delrole(ctx, *,role_name):
    guild = ctx.guild
    print("delrole run")
    selfRole = guild.roles
    print(selfRole)
    for role in selfRole:
        print(role)
        if role.name == role_name:
            print(role.id)
            print("------")
            await role.delete()
            await ctx.send("Role deleted")
    
# embed reference
@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="title ~~(did you know you can have markdown here too?)~~", colour=discord.Colour(botColor), url="https://discordapp.com", description="this supports [named links](https://discordapp.com) on top of the previously shown subset of markdown. ```\nyes, even code blocks```")

    embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_thumbnail(url="https://lh3.googleusercontent.com/proxy/FSxR-w6DAx_-36JlbDd4fKK4FVwGDtA9cGCTASBDs1iKWFKXtkFL4MsMRyuRaVo3BUIbqCdUIYKHEEe7C8uMmYRZ8kH4TQAK40j-HJochCZWHw")
    embed.set_author(name="author name", url="https://discordapp.com", icon_url="https://lh3.googleusercontent.com/proxy/FSxR-w6DAx_-36JlbDd4fKK4FVwGDtA9cGCTASBDs1iKWFKXtkFL4MsMRyuRaVo3BUIbqCdUIYKHEEe7C8uMmYRZ8kH4TQAK40j-HJochCZWHw")
    embed.set_footer(text="footer text", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="🤔", value="some of these properties have certain limits...")
    embed.add_field(name="😱", value="try exceeding some of them!")
    embed.add_field(name="🙄", value="an informative error should show up, and this view will remain as-is until all issues are fixed")
    embed.add_field(name="<:thonkang:219069250692841473>", value="these last two", inline=True)
    embed.add_field(name="<:thonkang:219069250692841473>", value="are inline fields", inline=True)

    await ctx.send(embed=embed)

# Run, bot, run!
bot.run(token)

# NEXT STEPS: 
'''
1. Make shit pretty.
    a. Text formatting [check]
    b. Cleaning up the "America/New_York" to be simply New York [check]
2. Accept commands via DM ONLY
    a. Create roles based off of commands 
    b. IP/system TZ tracking? 
3. Other features
    a. Time until, timer, countdown, reminders 
    b. Help thing 
    c. How to publish? Figure out higher-level organizational shit. 
4. Github
    a. Create README, etc. Maybe find someone to give feedback on the code?
    b. Implement .gitignore, other sensitive tokens and API keys
'''