import discord
import youtube_dl
from discord.ext.commands import bot

# create a client object
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# event handler for when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

# event handler for when a message is received
@client.event
async def on_message(message):
    if message.author == client.user:
        # don't respond to messages from the bot
        return
    # Check if the author of the message is in a voice channel
    if message.author.voice:
        # Get the voice channel that the author is in
        channel = message.author.voice.channel
    else:
        # The author is not in a voice channel, so do nothing
        return

    # if the message content starts with "!play", try to play the YouTube video
    if message.content.startswith('!play'):
        # get the YouTube URL from the message
        youtube_url = message.content.split(' ')[1]

        # use youtube-dl to download the audio from the video
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            audio_url = info['formats'][0]['url']

        # connect to the voice channel and play the audio
        channel = message.author.voice.channel
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio(audio_url))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.5

        async def check_empty_voice_channel():
            # Get the voice client associated with the bot
            voice_client = bot.voice_client

            # Check if the bot is connected to a voice channel
            if voice_client and voice_client.is_connected():
                # Get the members in the voice channel
                members = voice_client.channel.members

                # Check if there are no members in the voice channel
                if not members:
                    # Disconnect the bot from the voice channel
                    await voice_client.disconnect()

        # Create an event handler for the `on_voice_state_update` event that calls the check_empty_voice_channel function
        @bot.event
        async def on_voice_state_update(member, before, after):
            await check_empty_voice_channel()


# run the bot using the bot token
client.run('MTA0ODUxNzM3MTc0MjE0MjU1NA.Gtplov.6csB9orucmisX8R7hjrqyKF8iinQ_yyvj20IkU')
