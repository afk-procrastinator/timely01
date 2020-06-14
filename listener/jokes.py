import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import os
import settings
import time
import sys
import asyncio
import requests
import json

commandKey = 't!'
bot = commands.Bot(command_prefix=commandKey)
key = settings.OMDB
botColor = 0x176BD3


class JokesListener(commands.Cog):
    @bot.command()
    async def movie(self, ctx, *args):
        search = ("_".join(args))
        response = requests.get("http://www.omdbapi.com/?apikey={0}&t={1}".format(key, search))
        data = json.loads(response.text)
        #print(json.dumps(data, indent=4, sort_keys=True))
        title = data["Title"]
        released = data["Released"]
        rated = data["Rated"]
        type = data["Type"]
        runtime = data["Runtime"]
        genre = data["Genre"]
        director = data["Director"]
        plot = data["Plot"]
        awards = data["Awards"]
        poster = data["Poster"]
        metascore = data["Metascore"]
        imdbRating = data["imdbRating"]
        
        stringOne = """**Title:** {0}
        **Date released:** {1}
        **Age rating:** {2}
        **Runtime:** {3}
        **Genre:** {4}
        """.format(title, released, rated, runtime, genre)
        stringTwo = """**Director:** {0}
        **Plot description:** {1}
        **Awards:** {2}
        **Metascore:** {3}
        **IMDB rating:** {4}
        """.format(director, plot, awards, metascore, imdbRating)
        
        embed = discord.Embed(title="Movie search: {}".format(title), colour=discord.Colour(botColor))
        embed.set_thumbnail(url=poster)
        embed.add_field(name="🎞🎞🎞🎞🎞🎞", value=stringOne + stringTwo, inline = True)
        await ctx.send(embed = embed)
        
    @movie.error
    async def movie_error(self, ctx, error):
        embed = discord.Embed(title="Movie search error >:(", colour=discord.Colour(botColor))
        embed.add_field(name="🎞🎞🎞🎞🎞🎞", value="**Please retry with a different search input!** \n Syntax is: `t!movie` `query`")
        await ctx.send(embed = embed)
        
def setup(client):
    client.add_cog(JokesListener(client))
    print('JokesListener is Loaded') 