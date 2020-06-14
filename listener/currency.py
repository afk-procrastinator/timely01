import discord
from discord.ext import commands
from discord.utils import get
import os
import settings
import asyncio
import json
import requests
botColor = 0x176BD3


commandKey = 't!'
token = settings.TOKEN
bot = commands.Bot(command_prefix=commandKey)

currenciesFirst = '''
`CAD` : Canadian Dollar
`HKD` : Hong Kong Dollar
`ISK` : Iceland Krona	
`PHP` : Philippine Peso	
`DKK` : Danish Krone	
`HUF` : Forint [Hungary]
`CZK` : Czech Koruna	
`GBP` : British Pound 
`RON` : New Romanian Lee
`SEK` : Swedish Krona	
`IDR` : Rupiah [Indonesia]
`INR` : Indian Rupee
`BRL` : Brazilian Real	
`RUB` : Russian Ruble
`HRK` : Croatian Kuna	
`JPY` : Japanese Yen
'''

currenciesSecond = '''
`THB` : Bhat [Thailand]
`CHF` : Swiss Franc
`EUR` : Euro
`MYR` : Malaysian Ringgit	
`BGN` : Bulgarian Lev	
`TRY` : Turkish Lira	
`CNY` : Yuan Renminbi [China]
`NOK` : Norwegian Krone	
`NZD` : New Zealand Dollar
`ZAR` : Rand [Lesotho]
`USD` : United States Dollar
`SGD` : Singapore Dollar	
`AUD` : Australian Dollar
`ILS` : New Israeli Sheqel	
`KRW` : Won [Korea]
`PLN` : Zloty [Poland]
'''

async def getAPI(self, base, currency):
    response = requests.get("https://api.exchangeratesapi.io/latest?base={}".format(base))
    data = json.loads(response.text)
    return data["rates"][currency]

class CurrencyListener(commands.Cog):
    @bot.command()
    async def convert(self, ctx, amount, base: str, to: str, currency: str):
        base = base.upper()
        currency = currency.upper()
        response = await getAPI(self, base, currency)
        amount = int(amount)
        final = round((amount * response), 2)
        embed = discord.Embed(title="💸💸💸", colour=discord.Colour(botColor))
        embed.add_field(name = "Converting {0} to {1}".format(base, currency), value = "`{0}` `{1}` in `{2}` is \n `{3} {4}`".format(amount, base, currency, final, currency), inline=True)
        embed.set_footer(text = "Thanks to exchangeratesapi.io for the data!")
        await ctx.send(embed = embed)

    @convert.error
    async def convertError(self, ctx, error):
        embed = discord.Embed(title="Possible currencies:", colour=discord.Colour(botColor))
        embed.add_field(name="Syntax", value="`?convert` `amount` `original currency` `converted currency`", inline = False)
        embed.add_field(name = "-", value = currenciesFirst, inline=True)
        embed.add_field(name = "-", value = currenciesSecond, inline=True)
        embed.set_footer(text = "Thanks to exchangeratesapi.io for the data!")
        await ctx.send(embed = embed)
    
def setup(client):
    client.add_cog(CurrencyListener(client))
    print('CurrencyListener is Loaded') 