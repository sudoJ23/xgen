import discord, json, codecs, os, sys

class Commands():

    def __init__(self):
        return

    def restart(self):
        print("[ INFO ] RESTARTING BOT")
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def updateFromGit(self):
        os.system("git pull")
        restart()