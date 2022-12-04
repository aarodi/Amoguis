import discord
import youtube_dl
from discord.ext.commands import Bot

# create a client object
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# create a global queue for storing the YouTube URLs of videos to play
queue = []

# create a global variable for storing the current voice client
voice_client = None

# create a global variable for storing the current audio source
audio_source = None


# create an async function for playing the next video in the queue
async def play_next_video():
    global audio_source  # declare that audio_source is a global variable

    # check if the queue is not empty
    if queue:
        # get the next YouTube URL from the queue
        youtube_url = queue.pop(0)

        # use youtube-dl to download the audio from the video
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        try:
            # try to download the audio from the video
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                audio_url = info['formats'][0]['url']
        except youtube_dl.utils.DownloadError:
            # the video could not be downloaded, so display a message to the user and remove the video from the queue
            await channel.send(f'Unable to download video: {youtube_url}')
            return

        # play the audio from the next YouTube video
        audio_source = discord.FFmpegPCMAudio(audio_url)
        voice_client.play(audio_source)
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
        voice_client.source.volume = 0.5

        # check if the voice_client is already playing audio
        if voice_client.is_playing():
            # the voice_client is already playing audio, so do nothing
            return

        # play the audio
        voice_client.play(audio_source)

        # send a message with the video title
        await channel.send(f'Now playing: {info["title"]}')

    else:
        # the queue is empty, so disconnect from the voice channel
        await voice_client.disconnect()


# create a function for checking if the voice channel is empty
async def check_empty_voice_channel():
    # Get the list of guilds that the bot is connected to
    guilds = client.guilds

    # Get the first guild in the list
    guild = next(iter(guilds))

    # Get the voice client associated with the bot
    global voice_client
    voice_client = guild.voice_client

    # Check if the bot is connected to a voice channel
    if voice_client and voice_client.is_connected():
        # Get the members in the voice channel
        members = voice_client.channel.members

        # Check if there are no members in the voice channel except for the bot
        if len(members) == 1 and members[0] == client.user:
            # Disconnect the bot from the voice channel
            await voice_client.disconnect()


# event handler for when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    # Start the background task that checks for empty voice channels
    client.loop.create_task(check_empty_voice_channel())


# event handler for when a message is received
@client.event
async def on_message(message):
    global queue  # declare that queue is a global variable
    global audio_source  # declare that audio_source is a global variable
    global voice_client  # declare that voice_client is a global variable

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
        # check if the bot is already connected to a voice channel
        if voice_client and voice_client.is_connected():
            # the bot is already connected, so move the bot to the new voice channel
            await voice_client.move_to(channel)
        else:
            # the bot is not connected, so connect to the voice channel
            voice_client = await channel.connect()

        # add the YouTube URL to the queue
        youtube_url = message.content.split(' ')[1]
        queue.append(youtube_url)

        # play the next video in the queue
        await play_next_video()

    # if the message content starts with "!pause", pause the audio that is currently playing
    elif message.content.startswith('!pause'):
        if audio_source:
            audio_source.pause()

    # if the message content starts with "!resume", resume playing the audio that is currently paused
    elif message.content.startswith('!resume'):
        if audio_source:
            audio_source.resume()

    # if the message content starts with "!stop", stop playing the audio and clear the queue
    elif message.content.startswith('!stop'):
        queue.clear()

        if audio_source:
            audio_source.stop()

        # disconnect from the voice channel
        await voice_client.disconnect()


# run the bot using the bot token
client.run('LOL')
