import googlemaps
from timezonefinder import TimezoneFinder
import discord
from discord.ext import commands
from discord.utils import get
from dateutil import tz 
import arrow as ar
from dotenv import load_dotenv
import os
import settings

print(settings.GMAPS)
print(settings.TOKEN)

gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
bot = commands.Bot(command_prefix='?')
tf = TimezoneFinder()
lat = 0
lon = 0
region = ""
timeVibeRole = False

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
    return shifted

# tz command: takes one arg, gives time at location
@bot.command()
async def tz(ctx, input: str):
    shifted = timeZone(input)
    formatted = shifted.format("HH:mm:ss")
    region = region.split("/")[1].replace("_", " ")
    await ctx.send(f"Time in `{region}` is currently `{formatted}`.")

# only allows Admin to call the setup()
@bot.command()
# @commands.has_role("Power")
async def setup(ctx):
    guild = ctx.guild
    print("setup run")
    await guild.create_role(name="TimeVibeRole")
    selfRole = guild.roles
    print(selfRole)
    for role in selfRole:
        print(role)
        if role == "TimeVibeRole":
            print(role.id)
            timeVibeRole = True
            await ctx.send("Bot role already exists!")
            
# setup command error handling
@setup.error
async def setup_error(ctx, error):
    await ctx.send("Please give the bot permission to edit roles first!")

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

    await ctx.send(content="this `supports` __a__ **subset** *of* ~~markdown~~ 😃 ```js\nfunction foo(bar) {\n  console.log(bar);\n}\n\nfoo(1);```", embed=embed)

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