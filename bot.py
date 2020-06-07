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

commandKey = '?'
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
bot = commands.Bot(command_prefix=commandKey)
tf = TimezoneFinder()
lat = 0
lon = 0
region = ""
timeVibeRole = False
cancelTimer = False

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
    global cancelTimer
    if arg2 in ["seconds", "minutes", "hours", "minute", "hour", "m", "mins", "hr", "hrs"]:
        units = arg2
    else:
        embed = discord.Embed(title="Timer error:", colour=discord.Colour(0xffffff))
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
        embed = discord.Embed(title="Timer too long!", colour=discord.Colour(0xffffff))
        embed.add_field(name="Progress Bar", value="Your timer is over 12 hours! Why don't you try the `?reminder` command instead?")
        await ctx.send(embed=embed)
        return
    t = 0
    while t < arg1 + 1:
        if cancelTimer == True:
            string = ("_**CANCELLED_**")
            embed = discord.Embed(title="Timer:", colour=discord.Colour(0xffffff))
            embed.add_field(name="Progress Bar", value=string)
            return
        bar_length = 20
        percent = float(t) / arg1
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        timeRemaining = time.strftime("%H:%M:%S", time.gmtime(int(arg1-t)))
        string = ("```\rPercent: [{0}] {1}%```".format(arrow + spaces, int(round(percent * 100))))
        embed = discord.Embed(title="Timer: {0}".format(timeRemaining), colour=discord.Colour(0xffffff))
        embed.add_field(name="Progress Bar", value=string)
        if t == 0:
            message = await ctx.send(embed=embed)
        else:
            await message.edit(embed=embed)
        t += 1
        await asyncio.sleep(1)
    string = ("_**FINISHED**_")
    embed = discord.Embed(title="Timer:", colour=discord.Colour(0xffffff))
    embed.add_field(name="Progress Bar", value=string)
    await message.edit(embed=embed)

@bot.command()
async def cancelTimer(ctx):
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
    global lat, lon
    utc = ar.utcnow()
    testing = gmaps.geocode(input)
    lat = extract_values(testing, "lat")[0]
    lon = extract_values(testing, "lng")[0]
    region = tf.timezone_at(lng=lon, lat=lat)
    shifted = utc.to(region)
    formatted = shifted.format("HH:mm:ss")
    region = region.split("/")[1].replace("_", " ")
    embed = discord.Embed(title="**Timezone**", colour=discord.Colour(0xffffff))
    embed.add_field(name="Local time in:", value=region)
    await ctx.send(embed=embed)
#    await ctx.send(f"Time in `{region}` is currently `{formatted}`.")
    return

# tz error command handling
@tz.error
async def tz_error(ctx, error):
    print(error)

# only allows Admin to call the setup()
@bot.command()
# @commands.has_role("Power")
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
    embed = discord.Embed(title="**Argument error**", colour=discord.Colour(0xffffff))
    embed.add_field(name="Possible arguments:", value="`role` - creates role for bot, only needed for initialization.")
    await ctx.send(embed=embed)


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
    embed = discord.Embed(title="title ~~(did you know you can have markdown here too?)~~", colour=discord.Colour(0xffffff), url="https://discordapp.com", description="this supports [named links](https://discordapp.com) on top of the previously shown subset of markdown. ```\nyes, even code blocks```")

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
    a. Text formatting
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