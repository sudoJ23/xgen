import discord, json, codecs, sys
from .message import Message

configOpen = codecs.open('config.json', 'r', 'utf-8')
config = json.load(configOpen)

msg = Message()

class Client(discord.Client):
    async def on_ready(self):
        print("Logged on as {0}".format(self.user))

    async def on_message(self, message):
        if config['bot']['printMessage'] == "true":
            print('Message from {0.guild.name} sender {0.author} : {0.content}'.format(message))

        if message.author == client.user:
            return
        msg.checkMessage(message)