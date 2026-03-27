import discord, json, codecs, os, sys, subprocess, datetime, re
from collections import Counter
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

    # ── Security Monitoring ────────────────────────────────────────

    async def checkAttack(self, message):
        """Parse auth.log untuk mendeteksi brute-force / failed SSH login."""
        log_paths = ['/var/log/auth.log', '/var/log/secure']
        log_file = next((p for p in log_paths if os.path.exists(p)), None)

        if not log_file:
            await message.reply("File log auth tidak ditemukan (`/var/log/auth.log` atau `/var/log/secure`).")
            return

        try:
            result = subprocess.check_output(
                ['tail', '-n', '5000', log_file],
                stderr=subprocess.DEVNULL
            ).decode('utf-8', errors='ignore')
        except PermissionError:
            await message.reply("Bot tidak memiliki izin untuk membaca log. Jalankan bot sebagai root atau tambahkan ke grup `adm`.")
            return

        # Ambil IP dari baris "Failed password" dan "Invalid user"
        failed_ips = re.findall(r'Failed password.*?from\s+(\d+\.\d+\.\d+\.\d+)', result)
        invalid_ips = re.findall(r'Invalid user.*?from\s+(\d+\.\d+\.\d+\.\d+)', result)
        all_ips = failed_ips + invalid_ips
        total_attempts = len(all_ips)

        embed = discord.Embed(title="Deteksi Serangan SSH (5000 baris terakhir)", color=0xED4245)
        embed.add_field(name="Total Percobaan Gagal", value=str(total_attempts), inline=True)
        embed.add_field(name="IP Unik", value=str(len(set(all_ips))), inline=True)

        if all_ips:
            top_attackers = Counter(all_ips).most_common(10)
            lines = "\n".join([f"`{ip}` — **{count}x**" for ip, count in top_attackers])
            embed.add_field(name="Top 10 IP Penyerang", value=lines, inline=False)
        else:
            embed.add_field(name="Status", value="Tidak ditemukan percobaan login gagal.", inline=False)

        embed.set_footer(text=f"Sumber: {log_file}")
        await message.channel.send(embed=embed)

    async def fail2banStatus(self, message):
        """Tampilkan status fail2ban: jail aktif dan IP yang sedang di-ban."""
        try:
            # Cek semua jail yang aktif
            jails_raw = subprocess.check_output(
                ['fail2ban-client', 'status'],
                stderr=subprocess.DEVNULL
            ).decode('utf-8', errors='ignore')

            jail_names = re.findall(r'Jail list:\s+(.+)', jails_raw)
            if not jail_names:
                await message.reply("Fail2ban aktif tapi tidak ada jail yang ditemukan.")
                return

            jails = [j.strip() for j in jail_names[0].split(',')]
            embed = discord.Embed(title="Status Fail2ban", color=0xFEE75C)

            total_banned = 0
            for jail in jails:
                try:
                    detail = subprocess.check_output(
                        ['fail2ban-client', 'status', jail],
                        stderr=subprocess.DEVNULL
                    ).decode('utf-8', errors='ignore')

                    banned_count = re.search(r'Currently banned:\s+(\d+)', detail)
                    total_fail = re.search(r'Total failed:\s+(\d+)', detail)
                    banned_ips_raw = re.search(r'Banned IP list:\s+(.+)', detail)

                    count = int(banned_count.group(1)) if banned_count else 0
                    total_banned += count
                    fails = total_fail.group(1) if total_fail else "0"
                    banned_ips = banned_ips_raw.group(1).strip() if banned_ips_raw and banned_ips_raw.group(1).strip() else "Tidak ada"

                    value = f"Banned: **{count}** | Total gagal: **{fails}**\n`{banned_ips[:200]}`"
                    embed.add_field(name=f"Jail: {jail}", value=value, inline=False)
                except Exception:
                    embed.add_field(name=f"Jail: {jail}", value="Gagal membaca detail.", inline=False)

            embed.set_footer(text=f"Total IP ter-ban saat ini: {total_banned}")
            await message.channel.send(embed=embed)

        except FileNotFoundError:
            await message.reply("Fail2ban tidak terinstall atau tidak ditemukan di PATH.")
        except PermissionError:
            await message.reply("Bot tidak memiliki izin untuk menjalankan `fail2ban-client`.")
        except subprocess.CalledProcessError:
            await message.reply("Fail2ban tidak berjalan. Jalankan `sudo systemctl start fail2ban`.")

    async def activeConnections(self, message):
        """Tampilkan koneksi jaringan aktif, highlight port yang tidak umum."""
        COMMON_PORTS = {22, 80, 443, 3306, 5432, 6379, 27017, 8080, 8443}

        conns = psutil.net_connections(kind='inet')
        established = [c for c in conns if c.status == 'ESTABLISHED' and c.raddr]

        # Kelompokkan berdasarkan IP remote
        ip_counter = Counter(c.raddr.ip for c in established)
        suspicious = [
            c for c in established
            if c.laddr.port not in COMMON_PORTS and c.raddr.port not in COMMON_PORTS
        ]

        embed = discord.Embed(title="Koneksi Jaringan Aktif", color=0x5865F2)
        embed.add_field(name="Total Koneksi ESTABLISHED", value=str(len(established)), inline=True)
        embed.add_field(name="IP Remote Unik", value=str(len(ip_counter)), inline=True)
        embed.add_field(name="Koneksi Port Tidak Umum", value=str(len(suspicious)), inline=True)

        if suspicious:
            lines = []
            for c in suspicious[:10]:
                pid_info = f"PID {c.pid}" if c.pid else "PID ?"
                lines.append(f"`{c.laddr.ip}:{c.laddr.port}` → `{c.raddr.ip}:{c.raddr.port}` ({pid_info})")
            embed.add_field(name="Koneksi Mencurigakan (maks 10)", value="\n".join(lines), inline=False)

        if ip_counter:
            top_ips = ip_counter.most_common(5)
            lines = [f"`{ip}` — {count} koneksi" for ip, count in top_ips]
            embed.add_field(name="Top 5 IP Remote", value="\n".join(lines), inline=False)

        await message.channel.send(embed=embed)

    async def dockerStatus(self, message):
        """Tampilkan status semua Docker container."""
        try:
            # Ambil semua container (running + stopped)
            raw = subprocess.check_output(
                ['docker', 'ps', '-a', '--format',
                 '{{.Names}}\t{{.Status}}\t{{.Image}}\t{{.Ports}}'],
                stderr=subprocess.DEVNULL
            ).decode('utf-8', errors='ignore').strip()

            if not raw:
                await message.reply("Tidak ada Docker container yang ditemukan.")
                return

            containers = [line.split('\t') for line in raw.splitlines()]
            running = [c for c in containers if c[1].startswith('Up')]
            stopped = [c for c in containers if not c[1].startswith('Up')]

            embed = discord.Embed(title="Docker Containers", color=0x0db7ed)
            embed.add_field(name="Total", value=str(len(containers)), inline=True)
            embed.add_field(name="Running", value=str(len(running)), inline=True)
            embed.add_field(name="Stopped", value=str(len(stopped)), inline=True)

            if running:
                lines = []
                for c in running:
                    name, status, image, ports = (c + [''] * 4)[:4]
                    port_str = ports[:50] if ports else "-"
                    lines.append(f"🟢 **{name}** `{image}`\n　{status} | `{port_str}`")
                embed.add_field(name="Running Containers", value="\n".join(lines[:10]), inline=False)

            if stopped:
                lines = []
                for c in stopped:
                    name, status, image, ports = (c + [''] * 4)[:4]
                    lines.append(f"🔴 **{name}** `{image}` — {status}")
                embed.add_field(name="Stopped Containers", value="\n".join(lines[:10]), inline=False)

            # Ambil resource usage container yang running
            if running:
                stats_raw = subprocess.check_output(
                    ['docker', 'stats', '--no-stream', '--format',
                     '{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'],
                    stderr=subprocess.DEVNULL
                ).decode('utf-8', errors='ignore').strip()

                if stats_raw:
                    stat_lines = []
                    for line in stats_raw.splitlines():
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            stat_lines.append(f"`{parts[0]}` — CPU: **{parts[1]}** | RAM: **{parts[2]}**")
                    if stat_lines:
                        embed.add_field(name="Resource Usage", value="\n".join(stat_lines[:10]), inline=False)

            await message.channel.send(embed=embed)

        except FileNotFoundError:
            await message.reply("Docker tidak terinstall atau tidak ditemukan di PATH.")
        except PermissionError:
            await message.reply("Bot tidak memiliki izin untuk menjalankan Docker. Tambahkan user ke grup `docker`:\n```sudo usermod -aG docker namauser```")
        except subprocess.CalledProcessError:
            await message.reply("Gagal menjalankan perintah Docker. Pastikan Docker daemon berjalan:\n```sudo systemctl start docker```")

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
