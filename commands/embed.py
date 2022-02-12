from nextcord.ext import commands
import nextcord
import os


class Embed(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def embed(self, ctx, *, msg):
        embed = nextcord.Embed(title="", description=msg, color=0x00ff00)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Embed(client))
