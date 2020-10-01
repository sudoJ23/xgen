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
        # print("content : %s" % (message.content))
        # print("clean content : %s" % (message.clean_content))
        # print("\n%s" % (message.author))
        # print("\n%s" % (message.author.id))

        if message.clean_content == "":
            return

        self.prefix = message.clean_content[0]
        # self.split = message.clean_content.split(" ")
        content = message.clean_content.lower()

        if self.prefix != self.Prefix:
            return

        if "restart" in content:
            if str(message.author.id) in config['bot']['adminId']:
                self.command.restart()
        
        elif "updategit" in content:
            if str(message.author.id) in config['bot']['adminId']:
                await self.command.updateFromGit(message)

        elif "add" in content:
            print("\n")
            print(message)
            print(message.mentions)
            print("\n%s %s" % (message.mentions[0].name, message.mentions[0].id))
            print("\n%s %s" % (message.mentions[1].name, message.mentions[1].id))

        elif "say" in content:
            say = content.replace(self.prefix + "say ", "")
            await message.channel.send(say)

        elif "dm" in content:
            self.split = content.split(" ")
            self.dm = content.replace(self.split[0] + " " + self.split[1] + " ", "")
            # self.userId = split[1]
            # self.target = client.get_user(self.userId)
            self.target = message.mentions[0]
            print("\n======\n%s\nbot : %s\n\n%s\n\nmessage : %s\nmentions : %s\nuserId : %s\n" % (message.author, message.author.bot, message.mentions, self.dm, message.mentions[0], message.mentions[0].id))
            await self.target.create_dm()
            await self.target.dm_channel.send(self.dm)

        elif "join" in content:
            await self.command.joinVoice(message)

        elif "getallchannel" in content:
            self.channels = await self.guild.getAllChannel(message.guild)
            print(self.channels)
            message.reply(self.channels)

        elif "disconnect" in content:
            await self.command.disconnect(message)

        # elif "tes":
