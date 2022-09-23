import nextcord
from nextcord.ext import commands
import os
import pymongo
from webserver import keep_alive

# Set environment variables

intents = nextcord.Intents.all()
TOKEN = os.environ['TOKEN']


async def prefix_d(_, message):
    dbclient = pymongo.MongoClient(os.environ["mongoDBclient"])
    db = dbclient[str(message.guild.id)]
    prefix = db["prefix"]
    prefix_x = prefix.find_one({"_id": 0})
    if not prefix_x or str(message.guild.id) not in prefix_x:
        prefix.delete_one({"_id": 0})
        prefix.insert_one({"_id": 0, str(message.guild.id): "."})
        prefix_x = prefix.find_one({"_id": 0})
    if str(message.content).startswith(prefix_x[str(message.guild.id)]):
        return prefix_x[str(message.guild.id)]
    else:
        return str(client.user.id)


client = commands.Bot(command_prefix=prefix_d,
                                   intents=intents,
                                   help_command=None)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


for pyFile in os.listdir("./commands"):
    if pyFile.endswith(".py"):
        client.load_extension(f"commands.{pyFile[:-3]}")
        print(f"{pyFile[:-3]} | Loaded")

keep_alive()
try:
    client.run(os.getenv('TOKEN'))
except nextcord.errors.HTTPException:
    os.system("kill 1")
    os.system("python main.py")
    print("rate limit ! /n/nRestarting./n/n")
