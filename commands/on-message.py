import nextcord
from nextcord.ext import commands, menus
import json
import pymongo
import os


def blocked(msg, words: list):
    for word in words:
        if word in str(msg.content).lower():
            return True
    else:
        return False


class OnMessage(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_message(self, message):
        with open("bot_admin.json", "r") as f:
            admins = json.loads(f.read())["Admins"]
        if str(message.author.id) in admins:
            return
        if message.guild is None:
            return
        if message.author.bot:
            return
        cluster = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")["Guardzilla"]
        blockedWords = cluster["blockedwords"]
        log = blockedWords.find_one({"_id": 0})
        if not log:
            blockedWords.insert_one({"_id": 0   , str(message.guild.id): [0, []]})
            log = blockedWords.find_one({"_id": 0})
        try:
            blocked_true, words = log[str(message.guild.id)]
        except:
            log.update({str(message.guild.id): [0, []]})
            blockedWords.delete_one({"_id": 0})
            blockedWords.insert_one(log)
            blocked_true, words = log[str(message.guild.id)]
        if blocked_true:
            if blocked(message, words):
                await message.delete()
                ""
                await message.channel.send(f"The message deleted cuz its bad word ok? {message.author.mention}.",
                                           delete_after=5)
                return
        # suggestion chat
        suggestions = cluster["suggestions"]
        channels = suggestions.find_one({"_id": 0})
        if not channels:
            suggestions.insert_one({"_id": 0})
            channels = suggestions.find_one({"_id": 0})
        if str(message.guild.id) in channels:
            if channels[str(message.guild.id)][0] == str(message.channel.id):
                if str(message.content)[0] != 'r':
                    l = str("> " + str(message.content).replace('\n', "\n> "))
                    embed = nextcord.Embed(description=l, color=0x00ff00)
                    avatar_url = message.author.avatar.url
                    embed.set_author(
                        name=f"{message.author} Suggestion", icon_url=avatar_url)
                    embed.set_thumbnail(url=avatar_url)
                    embed.add_field(name="Up votes:", value="0 Vote")
                    embed.add_field(name="Down votes:", value="0 Vote")
                    if self.client.user.avatar:
                        embed.set_footer(
                            text="Wants to send suggestion? Simply type in this channel!", icon_url=self.client.user.avatar.url)
                    else:
                        embed.set_footer(
                            text="Wants to send suggestion? Simply type in this channel!")
                    msg = await message.channel.send(embed=embed)
                    check = self.client.get_emoji(932702977976836136)
                    uncheck = self.client.get_emoji(932702978031374457)
                    await msg.add_reaction(emoji=check)
                    await msg.add_reaction(emoji=uncheck)
                    channels[str(message.guild.id)][1][0].update(
                        {str(msg.id): [str(l), str(message.author.id)]})

                    suggestions.delete_one({"_id": 0})
                    suggestions.insert_one(channels)
                    try:
                        await message.delete()
                    except:
                        pass


def setup(client):
    client.add_cog(OnMessage(client))
