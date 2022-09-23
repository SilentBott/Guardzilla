from nextcord.ext import commands
import nextcord
import pymongo
from os import environ as getenv


class SuggestRoom(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="suggestionRoom")
    async def suggestRoom(self, ctx, channel=None):
        if channel is None:
            channel = ctx.channel.id
        try:
            channel = int(channel.split("<#")[-1].split(">")[0])
        except:
            await ctx.reply("Wrong id ")
            return

        channel = await ctx.guild.fetch_channel(str(channel))
        db = pymongo.MongoClient(getenv["mongoDBclient"])[str(
            ctx.message.guild.id)]
        suggestions = db["suggestionsRoom"]
        suggestionRoom = suggestions.find_one({"_id": 0})
        if suggestionRoom == channel:
            await ctx.reply("this is already the suggestion room")
        else:
            embed = nextcord.Embed(
                description=
                f"This channel {channel.mention} will be the suggestion room.",
                color=0x00ff00)
            await ctx.send(embed=embed)
        suggestions.delete_one({"_id": 0})
        suggestions.insert_one({"_id": 0, "id": str(channel.id)})
        await ctx.message.delete()


def setup(client):
    client.add_cog(SuggestRoom(client))
