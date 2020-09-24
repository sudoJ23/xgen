from .commands import Commands
import discord, json, codecs

configOpen = codecs.open('config.json', 'r', 'utf-8')
config = json.load(configOpen)

command = Commands()

class Message():

    def __init__(self):
        self.Prefix = config["bot"]["prefix"]
        return

    def checkMessage(self, message):
        self.prefix = message.content[0]
        if self.prefix != self.Prefix:
            return

        if "restart" in message.content:
            command.restart()
        
        elif "updateGit" in message.content:
            command.updateGit()

        return
    return