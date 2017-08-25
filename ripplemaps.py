import discord, asyncio, aiohttp, re
from discord.ext import commands
import download
import requests

bot = commands.Bot(command_prefix='!')

with open("./config.json", "r") as file:
    config = json.load(file)

def __init__(self, bot):
    self.bot = bot

@bot.event
async def on_message(message):
    author = message.author
    msg = message.content
    reg = re.match('https?:\/\/osu\.ppy\.sh\/([bs])\/([0-9]+)', msg)
    if msg.startswith('https://osu.ppy.sh/') or msg.startswith('http://osu.ppy.sh/'):
        if reg:
            idtype, bid = reg.groups()
            if idtype == "b":
                await bot.send_message(author, "Link must be https://osu.ppy.sh/s/ID")
                return
            try:
                bmap = download.login(bid)
            except:
                await bot.send_message(discord.Object(id=config["request_channel"]), "Failed to download map.")
                return

            u = requests.post("https://uguu.se/api.php?d=upload-tool", files={"file": (bid + ".osz", bmap)}, data={"name": bid + '.osz'}).text #wait was .text a thing ye
            await bot.send_message(discord.Object(id=config["beatmap_channel"]), "Beatmapsetid: {} requested by {}\n{}".format(bid, author.mention, u))
    else:
        await bot.process_commands(message)

@bot.command()
async def shutdown():
    await bot.say(":wave:")
    await bot.logout()
    await bot.close()

if __name__ == "__main__":
    bot.run(config["token"])