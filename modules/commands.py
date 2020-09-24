import discord, json, codecs, os

class Commands():

    def restart():
        print("[ INFO ] RESTARTING BOT")
        python = sys.executable
        os.execl(python, python, * sys.argv)
        return

    def updateFromGit():
        os.system("git pull")
        restart()
        return