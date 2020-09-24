import discord, json, os, codecs, sys

configOpen = codecs.open('config.json', 'r', 'utf-8')
config = json.load(configOpen)

class Client(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

        if message.author == client.user:
            return

        if message.content.startswith('>restart'):
            restart()
        elif message.content.startswith('>updateGit'):
            updateFromGit()

def restart():
    print("[ INFO ] RESTARTING BOT")
    python = sys.executable
    os.execl(python, python, * sys.argv)

def updateFromGit():
    os.system("git pull")
    restart()

client = Client()
client.run(config['bot']['token'])