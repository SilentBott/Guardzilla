from nextcord.ext import commands
import nextcord
import os
import json
import pymongo
import os


def bot_admin(ctx):
    with open("bot_admin.json", ) as f:
        data = json.loads(f.read())
    is_admin = str(ctx.message.author.id) in data["Admins"]
    return is_admin


class Role(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(bot_admin)
    async def reload(self, ctx, extension):
        if extension.lower() == "all":
            await ctx.reply("All loaded cogs will be reloaded:", delete_after=10)
            for pyFile in os.listdir("./commands"):
                try:
                    if pyFile.endswith(".py"):
                        self.client.reload_extension(f"commands.{pyFile[:-3]}")
                        await ctx.reply(f"Cog: {pyFile}\nreloaded successfully", delete_after=3)
                except (nextcord.ext.commands.errors.CommandInvokeError, nextcord.ext.commands.errors.ExtensionNotLoaded) as err:
                    print(err)
            return
        commands_names = []
        for pyFile in os.listdir("./commands"):
            if pyFile.endswith(".py"):
                commands_names.append(pyFile[:-3])
        try:
            self.client.reload_extension(f"commands.{extension}")
            await ctx.send(f"The {extension} cog reloaded successfully.")
        except (nextcord.ext.commands.errors.CommandInvokeError, nextcord.ext.commands.errors.ExtensionNotLoaded):
            if extension in commands_names:
                await ctx.send(f"There cog: {extension}\nis unloaded so we can't reload it")
            else:
                await ctx.send(f"There isn't any cog to reload with the name: {extension}.")
        os.system("clear")


def setup(client):
    client.add_cog(Role(client))
