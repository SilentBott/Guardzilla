import nextcord
from nextcord.ext import commands
import json
import os
import pymongo
import os
from keep_alive import keep_alive

# Set environment variables
# os.environ['info'] = "test:pass123"
# os.environ['TOKEN'] = "MY-AWSOME-TOKEN"


intents = nextcord.Intents.all()
TOKEN = os.environ['TOKEN']


async def prefix_d(_, message):
    f = pymongo.MongoClient(
        f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    cluster = f["Guardzilla"]
    prefix = cluster["prefix"]
    prefix_x = prefix.find_one({"_id": 0})
    if not prefix_x or str(message.guild.id) not in prefix_x:
        prefix.delete_one({"_id": 0})
        prefix.insert_one({"_id": 0, str(message.guild.id): "."})
        prefix_x = prefix.find_one({"_id": 0})
    if str(message.content).startswith(prefix_x[str(message.guild.id)]):
        return prefix_x[str(message.guild.id)]
    else:
        return str(client.user.id)

client = nextcord.ext.commands.Bot(
    command_prefix=prefix_d, intents=intents, help_command=None)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


for pyFile in os.listdir("./commands"):
    if pyFile.endswith(".py"):
        client.load_extension(f"commands.{pyFile[:-3]}")
        print(f"{pyFile[:-3]} | Loaded")

keep_alive()
client.run(TOKEN)
