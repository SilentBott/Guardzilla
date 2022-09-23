#import required modules
from nextcord.ext import commands
from googlesearch import search


class H(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command()
    async def h(self, ctx, *, question):
        url = ""
        #search and get the url
        for u in search(f"{question} site:stackoverflow.com", num_results=1):
            url = u
            break
        #send it
        await ctx.send(f"GOT U!!\nGo there :)\n{url}")


# add the command as cog
def setup(client):
    client.add_cog(H(client))
