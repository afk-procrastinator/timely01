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
from master import get_prefix
from howlongtobeatpy import HowLongToBeat
bot = commands.Bot(command_prefix=get_prefix)
key = settings.OMDB
from master import get_color


class JokesListener(commands.Cog):
    @bot.command()
    async def hltb(self, ctx, *args):
        color = int(get_color(bot, ctx.message))
        search = (" ".join(args))
        results = await HowLongToBeat().async_search(search)
        if results is not None and len(results) > 0:
            best_element = max(results, key=lambda element: element.similarity)    
            name = best_element.game_name
            image = best_element.game_image_url
            gameplayMain = best_element.gameplay_main
            gameplayMainUnit = best_element.gameplay_main_unit
            gameplayMainLabel = best_element.gameplay_main_label
            gameplayMainExtra = best_element.gameplay_main_extra
            gameplayMainExtraUnit = best_element.gameplay_main_extra_unit
            gameplayMainExtraLabel = best_element.gameplay_main_extra_label
            gameplayCompletionist = best_element.gameplay_completionist
            gameplayCompletionistUnit = best_element.gameplay_completionist_unit
            gameplayCompletionistLabel = best_element.gameplay_completionist_label
            mainString = "It will take **{0} {1}** to beat {2}".format(gameplayMain, gameplayMainUnit, gameplayMainLabel)
            mainExtraString = "It will take **{0} {1}** to beat {2}".format(gameplayMainExtra, gameplayMainExtraUnit, gameplayMainExtraLabel)
            completionsitString = "It will take **{0} {1}** to beat {2}".format(gameplayCompletionist, gameplayCompletionistUnit, gameplayCompletionistLabel)
            embed = discord.Embed(title="**How Long to Beat {}**".format(name), colour=discord.Colour(color))
            embed.set_thumbnail(url=image)
            embed.add_field(name="🕹🕹🕹", value = "{0} \n{1} \n{2}".format(mainString, mainExtraString, completionsitString))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="**Search Error**", colour = discord.Color(color))
            prefix = get_prefix(bot, ctx.message)
            embed.add_field(name = "_**Please try again!**_", value = "Your query returned no significant data. Please try again! \n \nExample: `{0}hltb Undertale`".format(prefix))
            message = await ctx.send(embed = embed)
            await asyncio.sleep(2)
            await message.delete()
    
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
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Movie search: {}".format(title), colour=discord.Colour(color))
        embed.set_thumbnail(url=poster)
        embed.add_field(name="🎞🎞🎞🎞🎞🎞", value=stringOne + stringTwo, inline = True)
        await ctx.send(embed = embed)   
    
    @movie.error
    async def movie_error(self, ctx, error):
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Movie search error >:(", colour=discord.Colour(color))
        embed.add_field(name="🎞🎞🎞🎞🎞🎞", value="**Please retry with a different search input!** \n Syntax is: `t!movie` `query`")
        await ctx.send(embed = embed)
        
    @hltb.error
    async def hltb_error(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        embed = discord.Embed(title="Videogame search error >:(", colour=discord.Colour(botColor))
        embed.add_field(name="🎞🎞🎞🎞🎞🎞", value="**Please retry with a different search input!** \n Syntax is: `{}hltb Undertale`".format(prefix))
        message = await ctx.send(embed = embed)
        await asyncio.sleep(2)
        await message.delete()
        
    @bot.command()
    async def qr(self, ctx, args):
        args = args.join("%20")
        url = "http://api.qrserver.com/v1/create-qr-code/?data={}&size=1000x1000".format(args)
        embed = discord.Embed(title="QR Generator:", colour=discord.Colour(botColor))
        embed.set_image(url=url)
        await ctx.send(embed = embed)   
        

def setup(client):
    client.add_cog(JokesListener(client))
    print('JokesListener is Loaded') 