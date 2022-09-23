#import the required modules
from nextcord.ext import commands
import os
import nextcord
import json


def bot_admin(ctx):
    with open("bot_admin.json", ) as f:
        data = json.loads(f.read())
    is_admin = str(ctx.message.author.id) in data["Admins"]
    return is_admin


class Load(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(bot_admin)
    async def load(self, ctx, extension):
        commands_names = []
        for pyFile in os.listdir("./commands"):
            if pyFile.endswith(".py"):
                commands_names.append(pyFile[:-3])
        try:
            self.client.load_extension(f"commands.{extension}")
            await ctx.send(f"The {extension} loaded successfully.")
        except (nextcord.ext.commands.errors.ExtensionNotFound,
                nextcord.ext.commands.errors.ExtensionAlreadyLoaded):
            if extension in commands_names:
                await ctx.send(f"The {extension} already loaded.")
            else:
                await ctx.send(
                    f"There isn't any cog with the name: {extension}.")


# add the command as cog
def setup(client):
    client.add_cog(Load(client))
