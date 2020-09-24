import discord, json, codecs, os

class Commands():

    def restart():
        print("[ INFO ] RESTARTING BOT")
        self.python = sys.executable
        os.execl(self.python, self.python, * sys.argv)
        return

    def updateFromGit():
        os.system("git pull")
        self.restart()
        return
    return