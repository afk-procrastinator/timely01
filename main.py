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
from master import get_prefix

asciiString = """
                        .s$$$Ss.
            .8,         $$$. _. .              ..sS$$$$$"  ...,.;
 o.   ,@..  88        =.$"$'  '          ..sS$$$$$$$$$$$$s. _;"'
  @@@.@@@. .88.   `  ` ""l. .sS$$.._.sS$$$$$$$$$$$$S'"'
   .@@@q@@.8888o.         .s$$$$$$$$$$$$$$$$$$$$$'
     .:`@@@@33333.       .>$$$$$$$$$$$$$$$$$$$$'
     .: `@@@@333'       ..>$$$$$$$$$$$$$$$$$$$'
      :  `@@333.     `.,   s$$$$$$$$$$$$$$$$$'
      :   `@33       $$ S.s$$$$$$$$$$$$$$$$$'
      .S   `Y      ..`  ,"$' `$$$$$$$$$$$$$$
      $s  .       ..S$s,    . .`$$$$$$$$$$$$.
      $s .,      ,s ,$$$$,,sS$s.$$$$$$$$$$$$$.
      / /$$SsS.s. ..s$$$$$$$$$$$$$$$$$$$$$$$$$.
     /`.`$$$$$dN.ssS$$'`$$$$$$$$$$$$$$$$$$$$$$$.
    ///   `$$$$$$$$$'    `$$$$$$$$$$$$$$$$$$$$$$.
   ///|     `S$$S$'       `$$$$$$$$$$$$$$$$$$$$$$.
  / /                      $$$$$$$$$$$$$$$$$$$$$.
                           `$$$$$$$$$$$$$$$$$$$$$s.
                            $$$"'        .?T$$$$$$$
                           .$'        ...      ?$$#\
                           !       -=S$$$$$s
                         .!       -=s$$'  `$=-_      :
                        ,        .$$$'     `$,       .|
                       ,       .$$$'          .        ,
                      ,     ..$$$'
                          .s$$$'                 `s     .
                   .   .s$$$$'                    $s. ..$s
                  .  .s$$$$'                      `$s=s$$$
                    .$$$$'                         ,    $$s
               `   " .$$'                               $$$
               ,   s$$'                              .  $$$s
            ` .s..s$'                                .s ,$$
             .s$$$'                                   "s$$$,
          -   $$$'                                     .$$$$.
        ."  .s$$s                                     .$',',$.
        $s.s$$$$S..............   ................    $$....s$s......
"""

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
    "listener.jokes",
    "listener.birthday"
]

print("activate!!!")

# On bot login, send info
@bot.event
async def on_ready():
    bot.remove_command('help')
    print("onready")
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
    #print(asciiString)
    await bot.change_presence(activity=discord.Game(name="the Voight Kampff test"))

@bot.event
async def on_guild_join(guild):
    with open('files/{}.json'.format(guild.id), 'w+') as f:
        startData = {"info":{"prefix" : ".", "color" : 0x176BD3}}
        json.dump(startData, f, indent = 4)
        
@bot.event
async def on_guild_remove(guild):
    os.remove("files/{}.json".format(guild.id))
    print("deleted:" + str(guild.id))
    

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
