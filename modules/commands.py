import discord, json, codecs, os, sys

class Commands():

    def __init__(self):
        return

    def restart(self):
        print("[ INFO ] RESTARTING BOT")
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def updateFromGit(self, message):
        message.channel.send(os.system("git pull"))
        self.restart()