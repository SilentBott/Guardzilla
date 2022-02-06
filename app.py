import nextcord
from nextcord.ext import commands
import json
import os


intents = nextcord.Intents.all()
TOKEN = os.environ['TOKEN']


async def prefix_d(_, message):
    with open("prefix.json", "r") as f:
        prefix_x = json.loads(f.read())
    if str(message.content).startswith(prefix_x[str(message.guild.id)]):
        return prefix_x[str(message.guild.id)]
    elif str(message.content).replace("!", "").startswith(str(client.user.mention)):
        if "!" in str(message.content):
            return f"<@!{client.user.id}>"
        else:
            return str(client.user.mention)
    else:
        return str(client.user.id)

client = nextcord.ext.commands.Bot(
    command_prefix=prefix_d, intents=intents, help_command=None)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    with open("bot.json", ) as f:
        r = json.loads(f.read())


for pyFile in os.listdir("./commands"):
    if pyFile.endswith(".py"):
        client.load_extension(f"commands.{pyFile[:-3]}")
        print(f"{pyFile[:-3]} | Loaded")


client.run(TOKEN)
