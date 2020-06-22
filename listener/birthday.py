import discord
from discord.ext import commands
from discord.utils import get
import arrow
from dotenv import load_dotenv
import os
import settings
import time
import sys
import asyncio
import json
import arrow
import re
from master import get_prefix
from master import get_color

bot = commands.Bot(command_prefix=get_prefix)
token = settings.TOKEN

def writeFile(combined, ctx, user):
    with open('files/{}.json'.format(ctx.guild.id), 'r+') as file:
        addData = {"usersbday":{str(user.id): combined}}
        data = json.load(file)
        data.update(addData)
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)

class BirthdayListener(commands.Cog):
    @bot.command()
    async def bdayset(self, ctx, *args):
        user = ctx.message.author
        combined = " ".join(args) # i.e. 3 Jan
        try:
            date = arrow.get(combined, "MMMM D")
            writeFile(combined, ctx, user)
            color = int(get_color(bot, ctx.message))
            embed = discord.Embed(title="Birthday set!", colour=discord.Colour(color))
            embed.add_field(name="🎂🎂🎂", value="Set to: {0}".format(date))
            await user.send(embed = embed)
        except ValueError:
            print("oopsie!")
            
    @bot.command()
    async def bday(self, ctx, user: discord.Member):
        userID = user.id
        userNick = user.nick
        color = int(get_color(bot, ctx.message))
        with open('files/{}.json'.format(ctx.guild.id), 'r') as file:
            try:
                data = json.load(file)
                birthday = data["usersbday"][str(userID)]
                date = birthday.capitalize()
                embed = discord.Embed(title="{0}'s Birthday:".format(userNick), colour=discord.Colour(color))
                embed.add_field(name="🎂🎂🎂", value="Their birthday is: **{0}**".format(date))
                await ctx.send(embed = embed)
            except KeyError:
                prefix = get_prefix(bot, ctx.message)
                embed = discord.Embed(title="No Birthday Set!", colour=discord.Colour(color))
                embed.add_field(name="🎂🎂🎂", value="{0} doesn't have a birthday set! Use `{1}bdayset MONTH DAY` to set it.".format(userNick, prefix))
                await ctx.send(embed = embed)

        

        

    

def setup(client):
    client.add_cog(BirthdayListener(client))
    print('BirthdayListener is Loaded') 