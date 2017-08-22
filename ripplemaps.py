import discord, asyncio, aiohttp, re, os
from discord.ext import commands
import download
import requests
#from datadog import statsd

Token = ""
beatmap_channel = ""
request_channel = ""

bot = commands.Bot(command_prefix='!')

def __init__(self, bot):
    self.bot = bot

@bot.event
async def on_message(message):
    author = message.author
    msg = message.content
    reg = re.match('https?:\/\/osu\.ppy\.sh\/([bs])\/([0-9]+)', msg)
    if msg.startswith('https://osu.ppy.sh/') or msg.startswith('http://osu.ppy.sh/'):
        #statsd.increment('bot.request')
        if reg:
            idtype, bid = reg.groups()
            if idtype == "b":
                await bot.send_message(author, "Link must be https://osu.ppy.sh/s/ID")
                return

            try:
                bmap = download.login(bid)
            except:
                await bot.send_message(discord.Object(id=request_channel), "Failed to download map.")
                return

            u = requests.post("https://uguu.se/api.php?d=upload-tool", files={"file": (bid + ".osz", bmap)}, data={"name": bid + '.osz'}).text
            await bot.send_message(discord.Object(id=beatmap_channel), "Beatmapsetid: {} requested by {}\n{}".format(bid, author.mention, u))

    else:
        await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(Token)