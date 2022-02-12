import json
import pymongo
from nextcord.ext import commands
import os
import nextcord
import os


def bot_admin(ctx):
    client = pymongo.MongoClient(
        f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    cluster = client["Guardzilla"]
    bot_admin = cluster["bot_admin"]
    admin = bot_admin.find_one({"_id": 0})
    is_admin = str(ctx.message.author.id) in admin["Admins"]
    return is_admin


class UnLoad(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(bot_admin)
    async def unload(self, ctx, extension):
        commands_names = []
        for pyFile in os.listdir("./commands"):
            if pyFile.endswith(".py"):
                commands_names.append(pyFile[:-3])
        try:
            self.client.unload_extension(f"commands.{extension}")
            await ctx.send(f"The {extension} unloaded successfully.")
        except (nextcord.ext.commands.errors.ExtensionNotLoaded, nextcord.ext.commands.errors.ExtensionNotFound) as r:
            if extension in commands_names:
                await ctx.send(f"The {extension} already unloaded.")
            else:
                await ctx.send(f"There isn't any cog with the name: {extension}.")


def setup(client):
    client.add_cog(UnLoad(client))
