from .commands import Commands
import discord, json, codecs

configOpen = codecs.open('config.json', 'r', 'utf-8')
config = json.load(configOpen)

class Message():

    def __init__(self):
        self.Prefix = config["bot"]["prefix"]
        command = Commands()
        return

    def checkMessage(self, message):
        print("Checking message")
        self.prefix = message.content[0]
        # if self.prefix != self.Prefix:
        #     return

        if "restart" in message.content:
            self.command.restart()
        
        elif "updateGit" in message.content:
            self.command.updateGit()

        return