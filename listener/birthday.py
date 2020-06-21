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
        except ValueError:
            print("oopsie!")

    

def setup(client):
    client.add_cog(BirthdayListener(client))
    print('BirthdayListener is Loaded') 