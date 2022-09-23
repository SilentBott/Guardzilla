# get the required modules
from nextcord.ext import commands
import nextcord


class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def embed(self, ctx, *, msg):
        # get the title of the message
        title = "" if len(msg.split('"')) <= 1 else msg.split('"')[1]
        #the description
        description = msg.replace(title, "").replace('"', '')
        #send the message
        embed = nextcord.Embed(title=title,
                               description=description,
                               color=0x00ff00)
        await ctx.send(embed=embed)

# add the command as cog
def setup(client):
    client.add_cog(Embed(client))
