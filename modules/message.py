from .commands import Commands
import discord, json, codecs

configOpen = codecs.open('config.json', 'r', 'utf-8')
config = json.load(configOpen)

class Message():

    def __init__(self):
        self.Prefix = config["bot"]["prefix"]
        self.command = Commands()

    def checkMessage(self, message):
        print("content : %s" % (message.content))
        print("clean content : %s" % (message.clean_content))

        if message.clean_content == "":
            return

        self.prefix = message.clean_content[0]
        # print(message.content)
        if self.prefix != self.Prefix:
            return

        if "restart" in message.content:
            self.command.restart()
        
        elif "updateGit" in message.content:
            self.command.updateFromGit()