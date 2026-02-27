from .commands import Commands
from .guild import Guild
import discord, json, codecs

configOpen = codecs.open('config.json', 'r', 'utf-8')
usersOpen = codecs.open('users.json', 'r', 'utf-8')

config = json.load(configOpen)
users = json.load(usersOpen)

class Message():

    def __init__(self):
        self.Prefix = config["bot"]["prefix"]
        self.command = Commands()

    async def checkMessage(self, message, client):
        if message.clean_content == "":
            return

        self.prefix = message.clean_content[0]
        content = message.clean_content.lower()

        if self.prefix != self.Prefix:
            return

        # ── Bot Management ─────────────────────────────────────────
        if "restart" in content:
            if str(message.author.id) in config['bot']['adminId']:
                self.command.restart()
            else:
                await message.reply("Kamu tidak memiliki izin untuk command ini.")

        elif "updategit" in content:
            if str(message.author.id) in config['bot']['adminId']:
                await self.command.updateFromGit(message)
            else:
                await message.reply("Kamu tidak memiliki izin untuk command ini.")

        # ── Help ───────────────────────────────────────────────────
        elif "help" in content:
            prefix = self.Prefix
            embed = discord.Embed(title="Daftar Command Bot", color=0x5865F2)
            embed.add_field(name="Informasi", value=(
                f"`{prefix}help` — Tampilkan daftar command\n"
                f"`{prefix}ping` — Cek latency bot\n"
                f"`{prefix}serverinfo` — Info server Discord\n"
                f"`{prefix}userinfo [@user]` — Info tentang user"
            ), inline=False)
            embed.add_field(name="Moderasi", value=(
                f"`{prefix}kick @user [alasan]` — Kick member\n"
                f"`{prefix}ban @user [alasan]` — Ban member\n"
                f"`{prefix}mute @user <menit>` — Timeout member\n"
                f"`{prefix}unmute @user` — Hapus timeout\n"
                f"`{prefix}warn @user <alasan>` — Beri peringatan\n"
                f"`{prefix}warnings @user` — Lihat daftar peringatan"
            ), inline=False)
            embed.add_field(name="Utilitas", value=(
                f"`{prefix}say <teks>` — Bot kirim ulang pesan\n"
                f"`{prefix}dm @user <pesan>` — Kirim DM ke user\n"
                f"`{prefix}add @user` — Tambah user ke daftar\n"
                f"`{prefix}getallchannel` — List semua text channel\n"
                f"`{prefix}getcat` — List semua kategori"
            ), inline=False)
            embed.add_field(name="Sistem (VPS)", value=(
                f"`{prefix}sysinfo` — CPU, RAM, disk, uptime mesin"
            ), inline=False)
            embed.add_field(name="Musik", value=(
                f"`{prefix}join` — Bot masuk voice channel kamu\n"
                f"`{prefix}play <url/judul>` — Putar musik dari YouTube\n"
                f"`{prefix}stop` — Hentikan musik\n"
                f"`{prefix}disconnect` — Bot keluar voice channel"
            ), inline=False)
            embed.add_field(name="Admin Only", value=(
                f"`{prefix}restart` — Restart bot\n"
                f"`{prefix}updategit` — Update dari git + restart"
            ), inline=False)
            await message.channel.send(embed=embed)

        # ── Ping ───────────────────────────────────────────────────
        elif content.strip() == self.Prefix + "ping":
            await self.command.ping(message, client)

        # ── Server Info ────────────────────────────────────────────
        elif "serverinfo" in content:
            await self.command.serverInfo(message)

        elif "userinfo" in content:
            await self.command.userInfo(message)

        # ── Moderasi ───────────────────────────────────────────────
        elif "kick" in content:
            if str(message.author.id) in config['bot']['adminId']:
                split = message.clean_content.split(" ", 2)
                reason = split[2] if len(split) > 2 else None
                await self.command.kickMember(message, reason)
            else:
                await message.reply("Kamu tidak memiliki izin untuk command ini.")

        elif "ban" in content:
            if str(message.author.id) in config['bot']['adminId']:
                split = message.clean_content.split(" ", 2)
                reason = split[2] if len(split) > 2 else None
                await self.command.banMember(message, reason)
            else:
                await message.reply("Kamu tidak memiliki izin untuk command ini.")

        elif "unmute" in content:
            if str(message.author.id) in config['bot']['adminId']:
                await self.command.unmuteMember(message)
            else:
                await message.reply("Kamu tidak memiliki izin untuk command ini.")

        elif "mute" in content:
            if str(message.author.id) in config['bot']['adminId']:
                split = message.clean_content.split(" ")
                try:
                    duration = int(split[2]) if len(split) > 2 else 10
                except ValueError:
                    duration = 10
                await self.command.muteMember(message, duration)
            else:
                await message.reply("Kamu tidak memiliki izin untuk command ini.")

        elif "warnings" in content:
            await self.command.showWarnings(message)

        elif "warn" in content:
            if str(message.author.id) in config['bot']['adminId']:
                split = message.clean_content.split(" ", 2)
                reason = split[2] if len(split) > 2 else None
                await self.command.warnMember(message, reason)
            else:
                await message.reply("Kamu tidak memiliki izin untuk command ini.")

        # ── Sistem / VPS ───────────────────────────────────────────
        elif "sysinfo" in content:
            if str(message.author.id) in config['bot']['adminId']:
                await self.command.sysInfo(message)
            else:
                await message.reply("Kamu tidak memiliki izin untuk command ini.")

        # ── Utilitas ───────────────────────────────────────────────
        elif "add" in content:
            if not message.mentions:
                await message.reply("Sebutkan user yang ingin ditambahkan. Contoh: `>add @user`")
                return
            await self.command.addUser(message)

        elif "say" in content:
            say = message.clean_content.split(" ", 1)[1] if " " in message.clean_content else ""
            await message.channel.send(say)

        elif "dm" in content:
            self.split = content.split(" ")
            self.dm = message.clean_content.split(" ", 2)[2] if len(message.clean_content.split(" ")) > 2 else ""
            self.target = message.mentions[0]
            await self.target.create_dm()
            await self.target.dm_channel.send(self.dm)

        elif "getallchannel" in content:
            self.channels = message.guild.text_channels
            channel_list = "\n".join([f"• {ch.name}" for ch in self.channels])
            await message.reply(f"**Text Channels:**\n{channel_list}")

        elif "getcat" in content:
            self.categories = message.guild.categories
            cat_list = "\n".join([f"• {cat.name}" for cat in self.categories])
            await message.reply(f"**Kategori:**\n{cat_list}")

        # ── Musik / Voice ──────────────────────────────────────────
        elif "join" in content:
            await self.command.joinVoice(message)

        elif "play" in content:
            split = message.clean_content.split(" ", 1)
            if len(split) < 2:
                await message.reply("Masukkan URL atau judul lagu. Contoh: `>play Never Gonna Give You Up`")
                return
            await self.command.playMusic(message, split[1])

        elif "stop" in content:
            await self.command.stopMusic(message)

        elif "disconnect" in content:
            await self.command.disconnect(message)
