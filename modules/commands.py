import discord, json, codecs, os, sys, subprocess

class Commands():

    def __init__(self):
        return

    def restart(self):
        print("[ INFO ] RESTARTING BOT")
        python = sys.executable
        os.execl(python, python, * sys.argv)

    async def updateFromGit(self, message):
        result = subprocess.check_output('git pull', shell=True)
        if "Already up to date." in result:
            await message.channel.send(str(result, "utf-8"))
            return
        else:
            await message.channel.send(str(result, "utf-8"))
            self.restart()