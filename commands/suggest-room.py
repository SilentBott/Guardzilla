import json
from nextcord.ext import commands
import nextcord


class SuggestRoom(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="suggest-room")
    async def suggest_room(self, ctx, channel=None):
        if channel is None:
            channel = ctx.channel.id
        try:
            channel = int(channel)
        except ValueError:
            channel = channel.split("<#")[1].split(">")[0]
        channel = await ctx.guild.fetch_channel(str(channel))
        with open("./suggestions.json", ) as f:
            sug = json.loads(f.read())
        if str(ctx.guild.id) in sug:
            if sug[str(ctx.guild.id)][0] == str(channel.id):
                pass
            else:
                sug[str(ctx.guild.id)] = [str(channel.id), [{}]]
            embed = nextcord.Embed(description=f"This channel {channel.mention} will be the suggestion room.",
                                   color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            sug.update({str(ctx.guild.id): [str(channel.id), [{}]]})
            embed = nextcord.Embed(description=f"This channel {channel.mention} will be the suggestion room.",
                                   color=0x00ff00)
            await ctx.send(embed=embed)
        with open("./suggestions.json", "w") as f:
            json.dump(sug, f)
        await ctx.message.delete()


def setup(client):
    client.add_cog(SuggestRoom(client))
