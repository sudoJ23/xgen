import discord, json, codecs, os, sys, subprocess
import yt_dlp

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

class Commands():

    def __init__(self):
        return

    def restart(self):
        print("[ INFO ] RESTARTING BOT")
        python = sys.executable
        os.execl(python, python, * sys.argv)

    async def updateFromGit(self, message):
        result = subprocess.check_output('git pull', shell=True)
        if "Already" in str(result):
            await message.channel.send(str(result, "utf-8"))
            return
        else:
            await message.channel.send(str(result, "utf-8"))
            self.restart()

    async def addUser(self, message):
        user = message.mentions[0]
        with codecs.open('users.json', 'r', 'utf-8') as f:
            data = json.load(f)

        user_ids = [u['id'] for u in data['users']]
        if str(user.id) in user_ids:
            await message.reply(f"**{user.name}** sudah ada di daftar.")
            return

        data['users'].append({'id': str(user.id), 'name': user.name})
        with codecs.open('users.json', 'w', 'utf-8') as f:
            json.dump(data, f, indent=4)

        await message.reply(f"**{user.name}** berhasil ditambahkan ke daftar.")

    async def joinVoice(self, message):
        if not message.author.voice or not message.author.voice.channel:
            await message.reply("Kamu harus berada di voice channel terlebih dahulu.")
            return
        if message.guild.voice_client:
            await message.reply("Bot sudah berada di voice channel.")
            return
        channel = message.author.voice.channel
        print("connecting to channel %s" % channel)
        await channel.connect()

    async def disconnect(self, message):
        voice_client = message.guild.voice_client
        if voice_client:
            await voice_client.disconnect()
        else:
            await message.reply("Bot tidak sedang berada di voice channel.")

    async def playMusic(self, message, query):
        if not message.author.voice or not message.author.voice.channel:
            await message.reply("Kamu harus berada di voice channel terlebih dahulu.")
            return

        voice_client = message.guild.voice_client
        if not voice_client:
            voice_client = await message.author.voice.channel.connect()

        if voice_client.is_playing():
            voice_client.stop()

        await message.reply(f"Mencari: **{query}**...")

        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ytdl:
            info = ytdl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            url = info['url']
            title = info.get('title', 'Unknown')

        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        voice_client.play(source)
        await message.reply(f"Memutar: **{title}**")

    async def stopMusic(self, message):
        voice_client = message.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await message.reply("Musik dihentikan.")
        else:
            await message.reply("Tidak ada musik yang sedang diputar.")
