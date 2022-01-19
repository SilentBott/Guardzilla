import nextcord
from nextcord.ext import commands
import json
import os
from datetime import datetime
from keep_alive import keep_alive


intents = nextcord.Intents.all()
TOKEN = process.env.TOKEN
commandsNames = []


async def prefix_d(_, message):
    if message.guild is None:
        if str(client.user.id) in str(message.content).split(' ')[0]:
            if "!" in str(message.content).split(' ')[0]:
                return str(message.content).split(' ')[0].split(">")[0] + ">"
            else:
                return str(client.user.id)
        else:
            return "!"
    with open("prefix.json", ) as file:
        prefix_x = json.loads(file.read())
    if str(client.user.id) in str(message.content).split(' ')[0] or "<@&{client.user.id}>" in str(message.content).split(' ')[0]:
        if "<@&" in str(message.content).split(' ')[0]:
            if str(message.content).split(" ")[-1] == ">":
                str(message.content).split(' ')[0].split(">")[0] + "> "
            else:
                return str(message.content).split(' ')[0].split(">")[0] + ">"
        elif "!" in str(message.content).split(' ')[0]:
            return str(message.content).split(' ')[0].split(">")[0] + ">"
        else:
            return str(client.user.id)
    guild = message.guild
    prefix = prefix_x[str(guild.id)]
    return prefix

client = nextcord.ext.commands.Bot(
    command_prefix=prefix_d, intents=intents, help_command=None)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    with open("bot.json", ) as f:
        r = json.loads(f.read())
    now = datetime.utcnow()
    now = now.strftime("%c")  # %-I:%-M:%-S %p -%Z\n%a, %Y/%-m/%-d
    r["last_reboot"] = now
    with open("bot.json", "w") as f:
        json.dump(r, f)


for pyFile in os.listdir("./commands"):
    if pyFile.endswith(".py"):
        client.load_extension(f"commands.{pyFile[:-3]}")
        commandsNames.append(pyFile[:-3])
        print(f"{pyFile[:-3]} | Loaded")


keep_alive()
client.run(TOKEN)
