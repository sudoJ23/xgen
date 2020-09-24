from modules import Client
import discord, json, os, codecs, sys

configOpen = codecs.open('config.json', 'r', 'utf-8')
config = json.load(configOpen)

client = Client()
client.run(config['bot']['token'])