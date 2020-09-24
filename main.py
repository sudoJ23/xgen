from modules import *
import discord, json, os, codecs, sys

configOpen = codecs.open('config.json', 'r', 'utf-8')
config = json.load(configOpen)

class Client(discord.Client):

    async def on_ready(self):
        print("Logged on as {0}".format(self.user))
        self.msg = Message()
        return

    async def on_message(self, message):
        if config['bot']['printMessage'] == "true":
            print('Message from {0.guild.name} sender {0.author} : {0.content}'.format(message))
            return

        if message.author == client.user:
            return

        self.msg.checkMessage(message)
        return

client = Client()
client.run(config['bot']['token'])