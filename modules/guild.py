import discord, json, os, codecs, sys

class Guild():

    def __init__(self):
        self.configOpen = codecs.open('config.json', 'r', 'utf-8')
        self.usersOpen = codecs.open('users.json', 'r', 'utf-8')
        self.guildsOpen = codecs.open('guilds.json', 'r', 'utf-8')
        self.config = json.load(self.configOpen)
        self.users = json.load(self.usersOpen)
        self.guilds = json.load(self.guildsOpen)

    def checkGuildData(self, guildId):
        if guildId in guilds['guilds']:
            return True
            