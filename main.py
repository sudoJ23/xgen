import discord, json, os, codecs

configOpen = codecs.open('config.json', 'r', 'utf-8')
config = json.load(settingsOpen)

class Client(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = Client()
client.run(config['bot']['token'])