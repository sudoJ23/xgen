import discord, json, codecs, os, sys, subprocess

class Commands():

    def __init__(self):
        return

    def restart(self):
        print("[ INFO ] RESTARTING BOT")
        python = sys.executable
        os.execl(python, python, * sys.argv)

    async def updateFromGit(self, message):
        str(result, "utf-8")) = subprocess.check_output('git pull', shell=True)
        if "Already" in result:
            await message.channel.send(result)
            return
        else:
            await message.channel.send(result)
            self.restart()