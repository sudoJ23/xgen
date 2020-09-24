import discord

class Client(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = Client()
client.run('NzQyMTcwOTk4MDE0NzM4NTAz.XzCOmg.Xh64t8uz1HyQ8VWFy3HtFHO5jHs')