from nextcord.ext import commands
import json
import pymongo
import os


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="chat-filter")
    async def chatfilter(self, ctx, allowed):
        client = pymongo.MongoClient(
        f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        blockedwords = cluster["blockedwords"]
        r = blockedwords.find_one({"_id": 0})
        if not r:
            blockedwords.insert_one({"_id": 0, str(ctx.guild.id): [0, []]})
            r = prefix.find_one({"_id": 0})
        if str(ctx.guild.id) not in r:
            blockedwords.insert_one({"_id": 0, str(ctx.guild.id): [0, []]})
            r = prefix.find_one({"_id": 0})

        is_allowed = r[str(ctx.guild.id)][0]
        allowed = allowed[0].lower()
        if allowed in ["d", "a", '1', '0', 't', 'f']:
            if allowed in ["d", 'f', '0']:
                allowed = 0
            elif allowed in ["a", 't', '1']:
                allowed = 1
            if allowed == is_allowed:
                await ctx.reply(f"The chat filter is already set to: {'allowed' if allowed else 'disabled'} mode")
            else:
                r[str(ctx.guild.id)][0] = allowed
                blockedwords.delete_one({"_id": 0})
                blockedwords.insert_one(r)
                await ctx.reply(f"The chat filter set to: {'allowed' if allowed else 'disabled'} mode")
        else:
            await ctx.reply("")


def setup(client):
    client.add_cog(Admin(client))
