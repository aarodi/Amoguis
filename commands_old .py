import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="$")


client = discord.Client()


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot)) 
    

@bot.command()
async def ping(ctx, arg):
    await ctx.send("<@" + str(arg) + ">")
    


bot.run("")