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
from listener.reminder import runLoop

def get_prefix(client, message):
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_prefix)
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
bot.remove_command("help")
tf = TimezoneFinder()

month = ["months", "month", "mo", "mos"]
week = ["weeks", "week", "wk", "wks"]
day = ["days", "day", "dy", "dys"]
hour = ["hours", "hour", "hr", "hrs"]
min = ["minutes", "minute", "min", "mins"]

startup_extensions = [
    "listener.listener",
    "listener.timeZone",
    "listener.reminder",
    "listener.distance",
    "listener.timer",
    "listener.currency",
    "listener.botCommands",
    "listener.jokes"
]

# On bot login, send info
@bot.event
async def on_ready():
    bot.remove_command('help')
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    print('\nLogged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="a game"))

@bot.event
async def on_guild_join(guild):
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)    
    prefixes[str(guild.id)] = '.'
    with open('prefix.json', 'w' ) as f:
        json.dump(prefixes, f, indent = 4)
        
@bot.event
async def on_guild_remove(guild):
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)    
    prefixes.pop(str(guild.id))
    with open('prefix.json', 'w' ) as f:
        json.dump(prefixes, f, indent = 4)
        
@bot.command()
async def prefix(ctx, prefix):
    with open('prefix.json', 'r') as f:
        prefixes = json.load(f)    
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefix.json', 'w' ) as f:
        json.dump(prefixes, f, indent = 4)

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

# Run, bot, run!
bot.run(token)
