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

        if "restart" in content:
            if str(message.author.id) in config['bot']['adminId']:
                self.command.restart()

        elif "updategit" in content:
            if str(message.author.id) in config['bot']['adminId']:
                await self.command.updateFromGit(message)

        elif "help" in content:
            prefix = self.Prefix
            help_text = (
                f"**Daftar Command Bot**\n"
                f"`{prefix}help` — Tampilkan daftar command\n"
                f"`{prefix}say <teks>` — Bot kirim ulang pesan\n"
                f"`{prefix}dm @user <pesan>` — Kirim DM ke user\n"
                f"`{prefix}add @user` — Tambah user ke daftar\n"
                f"`{prefix}join` — Bot masuk voice channel kamu\n"
                f"`{prefix}disconnect` — Bot keluar voice channel\n"
                f"`{prefix}play <url/judul>` — Putar musik dari YouTube\n"
                f"`{prefix}stop` — Hentikan musik\n"
                f"`{prefix}getallchannel` — List semua text channel\n"
                f"`{prefix}getcat` — List semua kategori\n"
                f"`{prefix}restart` — Restart bot *(admin only)*\n"
                f"`{prefix}updategit` — Update dari git + restart *(admin only)*"
            )
            await message.channel.send(help_text)

        elif "add" in content:
            if not message.mentions:
                await message.reply("Sebutkan user yang ingin ditambahkan. Contoh: `>add @user`")
                return
            await self.command.addUser(message)

        elif "say" in content:
            say = content.replace(self.prefix + "say ", "")
            await message.channel.send(say)

        elif "dm" in content:
            self.split = content.split(" ")
            self.dm = content.replace(self.split[0] + " " + self.split[1] + " ", "")
            self.target = message.mentions[0]
            await self.target.create_dm()
            await self.target.dm_channel.send(self.dm)

        elif "join" in content:
            await self.command.joinVoice(message)

        elif "play" in content:
            self.split = message.clean_content.split(" ", 1)
            if len(self.split) < 2:
                await message.reply("Masukkan URL atau judul lagu. Contoh: `>play Never Gonna Give You Up`")
                return
            query = self.split[1]
            await self.command.playMusic(message, query)

        elif "stop" in content:
            await self.command.stopMusic(message)

        elif "getallchannel" in content:
            self.channels = message.guild.text_channels
            channel_list = "\n".join([f"• {ch.name}" for ch in self.channels])
            await message.reply(f"**Text Channels:**\n{channel_list}")

        elif "getcat" in content:
            self.categories = message.guild.categories
            cat_list = "\n".join([f"• {cat.name}" for cat in self.categories])
            await message.reply(f"**Kategori:**\n{cat_list}")

        elif "disconnect" in content:
            await self.command.disconnect(message)
