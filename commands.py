import discord
from discord import message
from discord.ext import commands
import json
import requests
from requests.models import Response
import datetime

bot = commands.Bot(command_prefix="$")


client = discord.Client()


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot)) 
    

@bot.command()
async def ping(ctx, arg):
    await ctx.send("<@" + str(arg) + ">")
    

@bot.command()
async def mping(ctx, arg1, arg2):
    for x in range(0, int(arg1)):
        #await ctx.send("<@" + str(arg2) + ">")
        await ctx.send(f"<@{str(arg2)}>")


@bot.command()
async def apifetch(ctx, func : str):
    await ctx.send("Fetching data")
    url = "http://71.45.152.38:3000/" + func
    # Do the HTTP get request
    response = requests.get(url)
    # Decode the JSON response into a dictionary and use the data
    rcv = json.dumps(response.json(), indent=4)
    info = "url = " + url + "\n"
    await ctx.send("```json\n" + info + rcv + "```")
    
@bot.command()
async def latency(ctx):
    await ctx.send(f'My ping is {round(bot.latency*1000,1)}ms')
    
@bot.command()
async def setstatus(ctx, arg):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=arg))

    
bot.run("nope :D")