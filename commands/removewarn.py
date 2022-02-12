import json
from nextcord.ext import commands
import nextcord
import pymongo
import os


class RemoveWarn(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def removewarn(self, ctx, member, number=0):
        try:
            member = str(int(member))
        except ValueError:
            member = member.split("<@")[1].split(">")[0].replace("!", "")
        member = await ctx.guild.fetch_member(member)

        embed = nextcord.Embed(color=0x00ff00)
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        warns = cluster["warns"]
        warnings = warns.find_one({"_id": 0})

        if str(ctx.guild.id) in warnings:
            if str(member.id) in warnings[str(ctx.guild.id)]:
                try:
                    removed = warnings[str(ctx.guild.id)
                                       ][str(member.id)][number-1]
                    warnings[str(ctx.guild.id)][str(member.id)].pop(number-1)
                    embed.add_field(
                        name=f"Removing the warn num {number}.\nFrom The user: {member.display_name} | {member.id}", value="_ _")
                    if not warnings[str(ctx.guild.id)][str(member.id)]:
                        warnings[str(ctx.guild.id)].pop(str(member.id))
                    warns.delete_one({"_id": 0})
                    warns.insert_one(warnings)
                except IndexError:
                    embed.add_field(
                        name=f"Wrong index.", value="_ _")
            else:
                embed.add_field(
                    name=f"The member: {member.display_name} | {member.id}:\nDoesn't have any warnings.", value="_ _")
        else:
            embed.add_field(
                name=f"The member: {member.display_name} | {member.id}:\nDoesn't have any warnings.", value="_ _")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(RemoveWarn(client))
