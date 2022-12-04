import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import craftscript
import time
from keep_alive import keep_alive
import pafy

prefix="!"
bot = commands.Bot(command_prefix=prefix, activity=discord.Activity(type=discord.ActivityType.watching, name=f"for {prefix}help"))
client = discord.Client()

@client.event
# Print when the program is ready for input
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  
@bot.command(name="craft",
      description="To use craft follow this order:\n" \
      "\tComplexity: 1 (very simple), 2 (simple), 3 (moderate), 4 (complex), 5 (very complex)\n" \
      "\tCraft Rank\n" \
      "\tCraft Mod\n" \
      "\tMisc Mod\n" \
      "\tTools: 1 (improvised), 2 (regular), 3 (masterwork)\n" \
      "\tIs Masterwork: 0 (no), 1 (yes)\n" \
      "\tItem Material: 'name', 'na' (no name)\n" \
      "\tIs Alchemy: 0 (no), 1 (yes)")
# crafting menu
async def craft(ctx, complexity, craft_rank, craft_mod, misc_mod, player_tools, is_masterwork, item_material, is_alchemy):
  # if not help, try and run the command
  try:
    if item_material == "na":
      item_material = ""
      is_special = 0
    else:
      is_special = 1

    await ctx.send(craftscript.main(complexity, craft_rank, craft_mod, misc_mod, player_tools, is_masterwork, item_material, is_special, is_alchemy))
  except:
    #if it fails, print error message
    await ctx.send("I am sorry, I had an error while trying to run that command...")


#audio commands
@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command(aliases=['p', 'pla'])
async def play(ctx, url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'):
  video = pafy.new(url)
  best = video.getbest()
  playurl = best.url
  time.sleep(2)
  global player
  channel = ctx.message.author.voice.channel
  try:
      player = await channel.connect()
  except:
      pass
  player.play(FFmpegPCMAudio(playurl))


@bot.command(aliases=['s', 'sto'])
async def stop(ctx):
  try:
    player.stop()
  except:
    print("error stopping")


@bot.command()
async def test(ctx, *args):
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" ".join(args)))

keep_alive()
bot.run(os.environ['TOKEN'])