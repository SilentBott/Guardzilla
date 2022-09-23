from nextcord.ext import commands
import nextcord
import pymongo
from os import environ as getenv

msgs = {}


class ReactionRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command(name="reaction-role")
    async def reaction_role(self, ctx, msg_id: int, emoji: nextcord.Emoji,
                            role: nextcord.Role):
        global msgs
        if ctx.author.top_role > role or ctx.author.id == ctx.guild.owner.id:
            msg = await ctx.fetch_message(msg_id)
            await msg.add_reaction(emoji=emoji)

            db = pymongo.MongoClient(
                getenv["mongoDBclient"])[ctx.message.guild.id]
            reaction_roles = db["reaction_roles"]
            r = reaction_roles.find_one({"_id": 0})
            if not r:
                reaction_roles.insert_one({"_id": 0})
                r = reaction_roles.find_one({"_id": 0})
            if str(ctx.guild.id) not in r:
                reaction_roles.insert_one({"_id": 0})
                r = reaction_roles.find_one({"_id": 0})

            r.update({str(msg_id): [int(emoji.id), int(role.id)]})
            reaction_roles.delete_one({"_id": 0})
            reaction_roles.insert_one(r)


def setup(client):
    client.add_cog(ReactionRole(client))
