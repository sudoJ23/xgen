from .commands import Commands
import discord, json, codecs

configOpen = codecs.open('config.json', 'r', 'utf-8')
config = json.load(configOpen)

class Message():

    def __init__(self):
        self.Prefix = config["bot"]["prefix"]
        self.command = Commands()

    def checkMessage(self, message):
        # print("Checking message")
        print(message.content)
        print(message.clean_content)
        self.prefix = message.content[0]
        # print(message.content)
        if self.prefix != self.Prefix:
            return

        if "restart" in message.content:
            self.command.restart()
        
        elif "updateGit" in message.content:
            self.command.updateFromGit()