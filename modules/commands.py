import discord, json, codecs, os, sys, subprocess, datetime
import yt_dlp
import psutil

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

    # ── Bot Management ─────────────────────────────────────────────

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

    # ── User Management ────────────────────────────────────────────

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

    # ── Discord Server Info ────────────────────────────────────────

    async def serverInfo(self, message):
        guild = message.guild
        online = sum(1 for m in guild.members if m.status != discord.Status.offline)
        created = guild.created_at.strftime("%d %b %Y")

        embed = discord.Embed(title=f"Info Server: {guild.name}", color=0x5865F2)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Region", value=str(guild.preferred_locale), inline=True)
        embed.add_field(name="Dibuat", value=created, inline=True)
        embed.add_field(name="Total Member", value=guild.member_count, inline=True)
        embed.add_field(name="Member Online", value=online, inline=True)
        embed.add_field(name="Bot", value=sum(1 for m in guild.members if m.bot), inline=True)
        embed.add_field(name="Text Channel", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice Channel", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Kategori", value=len(guild.categories), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        await message.channel.send(embed=embed)

    async def userInfo(self, message):
        user = message.mentions[0] if message.mentions else message.author
        member = message.guild.get_member(user.id)
        joined = member.joined_at.strftime("%d %b %Y") if member.joined_at else "Tidak diketahui"
        created = user.created_at.strftime("%d %b %Y")
        roles = [r.mention for r in member.roles if r.name != "@everyone"]
        roles_str = ", ".join(roles) if roles else "Tidak ada"

        embed = discord.Embed(title=f"Info User: {user.name}", color=0x57F287)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "-", inline=True)
        embed.add_field(name="Bot", value="Ya" if user.bot else "Tidak", inline=True)
        embed.add_field(name="Bergabung ke server", value=joined, inline=True)
        embed.add_field(name="Akun dibuat", value=created, inline=True)
        embed.add_field(name="Roles", value=roles_str, inline=False)
        await message.channel.send(embed=embed)

    # ── Moderation ─────────────────────────────────────────────────

    async def kickMember(self, message, reason):
        if not message.mentions:
            await message.reply("Sebutkan user yang ingin di-kick. Contoh: `>kick @user alasan`")
            return
        target = message.mentions[0]
        try:
            await target.kick(reason=reason or "Tidak ada alasan")
            embed = discord.Embed(description=f"**{target.name}** telah di-kick.\nAlasan: {reason or 'Tidak ada alasan'}", color=0xFEE75C)
            await message.channel.send(embed=embed)
        except discord.Forbidden:
            await message.reply("Bot tidak memiliki izin untuk kick member ini.")

    async def banMember(self, message, reason):
        if not message.mentions:
            await message.reply("Sebutkan user yang ingin di-ban. Contoh: `>ban @user alasan`")
            return
        target = message.mentions[0]
        try:
            await target.ban(reason=reason or "Tidak ada alasan")
            embed = discord.Embed(description=f"**{target.name}** telah di-ban.\nAlasan: {reason or 'Tidak ada alasan'}", color=0xED4245)
            await message.channel.send(embed=embed)
        except discord.Forbidden:
            await message.reply("Bot tidak memiliki izin untuk ban member ini.")

    async def muteMember(self, message, duration_minutes):
        if not message.mentions:
            await message.reply("Sebutkan user yang ingin di-mute. Contoh: `>mute @user 10`")
            return
        target = message.guild.get_member(message.mentions[0].id)
        try:
            duration = datetime.timedelta(minutes=duration_minutes)
            await target.timeout(duration, reason="Dimute oleh admin")
            embed = discord.Embed(description=f"**{target.name}** telah di-mute selama **{duration_minutes} menit**.", color=0xFEE75C)
            await message.channel.send(embed=embed)
        except discord.Forbidden:
            await message.reply("Bot tidak memiliki izin untuk mute member ini.")

    async def unmuteMember(self, message):
        if not message.mentions:
            await message.reply("Sebutkan user yang ingin di-unmute. Contoh: `>unmute @user`")
            return
        target = message.guild.get_member(message.mentions[0].id)
        try:
            await target.timeout(None)
            embed = discord.Embed(description=f"**{target.name}** telah di-unmute.", color=0x57F287)
            await message.channel.send(embed=embed)
        except discord.Forbidden:
            await message.reply("Bot tidak memiliki izin untuk unmute member ini.")

    async def warnMember(self, message, reason):
        if not message.mentions:
            await message.reply("Sebutkan user yang ingin diberi peringatan. Contoh: `>warn @user alasan`")
            return
        if not reason:
            await message.reply("Masukkan alasan peringatan. Contoh: `>warn @user spam`")
            return
        target = message.mentions[0]
        with codecs.open('warnings.json', 'r', 'utf-8') as f:
            data = json.load(f)

        uid = str(target.id)
        if uid not in data['warnings']:
            data['warnings'][uid] = []
        data['warnings'][uid].append({
            'reason': reason,
            'by': str(message.author.id),
            'at': datetime.datetime.utcnow().strftime("%d %b %Y %H:%M UTC")
        })
        with codecs.open('warnings.json', 'w', 'utf-8') as f:
            json.dump(data, f, indent=4)

        total = len(data['warnings'][uid])
        embed = discord.Embed(description=f"**{target.name}** mendapat peringatan ke-**{total}**.\nAlasan: {reason}", color=0xFEE75C)
        await message.channel.send(embed=embed)

    async def showWarnings(self, message):
        if not message.mentions:
            await message.reply("Sebutkan user yang ingin dilihat peringatannya. Contoh: `>warnings @user`")
            return
        target = message.mentions[0]
        with codecs.open('warnings.json', 'r', 'utf-8') as f:
            data = json.load(f)

        uid = str(target.id)
        warns = data['warnings'].get(uid, [])
        if not warns:
            await message.reply(f"**{target.name}** tidak memiliki peringatan.")
            return

        embed = discord.Embed(title=f"Peringatan untuk {target.name}", color=0xED4245)
        for i, w in enumerate(warns, 1):
            embed.add_field(name=f"#{i} — {w['at']}", value=w['reason'], inline=False)
        await message.channel.send(embed=embed)

    # ── VPS / System Monitoring ────────────────────────────────────

    async def sysInfo(self, message):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        uptime_sec = datetime.datetime.now().timestamp() - psutil.boot_time()
        uptime = str(datetime.timedelta(seconds=int(uptime_sec)))

        embed = discord.Embed(title="System Info", color=0x5865F2)
        embed.add_field(name="CPU Usage", value=f"{cpu}%", inline=True)
        embed.add_field(name="RAM Usage", value=f"{ram.percent}% ({ram.used // 1024**2} MB / {ram.total // 1024**2} MB)", inline=True)
        embed.add_field(name="Disk Usage", value=f"{disk.percent}% ({disk.used // 1024**3} GB / {disk.total // 1024**3} GB)", inline=True)
        embed.add_field(name="Uptime", value=uptime, inline=True)
        await message.channel.send(embed=embed)

    async def ping(self, message, client):
        latency = round(client.latency * 1000)
        embed = discord.Embed(description=f"Pong! Latency: **{latency}ms**", color=0x57F287)
        await message.channel.send(embed=embed)

    # ── Voice / Music ──────────────────────────────────────────────

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
