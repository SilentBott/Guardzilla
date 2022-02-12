from nextcord.ext import commands
import nextcord


class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command()
    async def ping(self, ctx):
        embed = nextcord.Embed(
            title=f"Pong!", description=f"Bot Latency:\n{round(self.client.latency * 1000)}ms", color=0x00ff00)
        if self.client.user.avatar:
            embed.set_thumbnail(url=self.client.user.avatar.url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Ping(client))
