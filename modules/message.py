from .commands import Commands
import discord, json, codecs

configOpen = codecs.open('config.json', 'r', 'utf-8')
usersOpen = codecs.open('users.json', 'r', 'utf-8')

config = json.load(configOpen)
users = json.load(usersOpen)

class Message():

    def __init__(self):
        self.Prefix = config["bot"]["prefix"]
        self.command = Commands()

    async def checkMessage(self, message):
        print("content : %s" % (message.content))
        print("clean content : %s" % (message.clean_content))

        if message.clean_content == "":
            return

        self.prefix = message.clean_content[0]
        split = message.clean_content.split(" ")
        content = message.clean_content
        author = message.author.id

        if self.prefix != self.Prefix:
            return

        if "restart" in content:
            if author in config['bot']['adminId']:
                self.command.restart(message)
        
        elif "updateGit" in content:
            if author in config['bot']['adminId']:
                await self.command.updateFromGit(message)

        elif "add" in content:
            print("\n")
            print(message)
            print(message.mentions)
            print("\n%s %s" % (message.mentions[0].name, message.mentions[0].id))
            print("\n%s %s" % (message.mentions[1].name, message.mentions[1].id))

        # elif "tes":
