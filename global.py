import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import json


def get_prefix(client, message):
    with open('files/prefix.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]