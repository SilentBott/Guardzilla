import nextcord
from nextcord.ext import commands, menus
import json


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
        # bad words
        if message.guild is None:
            return
        if message.author.bot:
            return
        try:
            with open("./blockedWords.json", "r") as f:
                blocked_true, words = json.loads(
                    f.read())[str(message.guild.id)]
        except:
            with open("./blockedWords.json", "r") as f:
                o = json.loads(f.read())
            with open("./blockedWords.json", "w") as ff:
                o.update(
                    {str(message.guild.id): [0, []]})
                json.dump(o, ff)
            with open("./blockedWords.json", "r") as f:
                blocked_true, words = json.loads(
                    f.read())[str(message.guild.id)]
        if blocked_true:
            if blocked(message, words):
                await message.delete()
                ""
                await message.channel.send(f"The message deleted cuz its bad word ok? {message.author.mention}.",
                                           delete_after=5)
                return
        # suggestion chat
        with open("./suggestions.json", "r") as f:
            channels = json.loads(f.read())
        if str(message.guild.id) in channels:
            if channels[str(message.guild.id)][0] == str(message.channel.id):
                if str(message.content)[0] == 'r' and str(message.author.id) in ["821486817957642242", "714941410716942419", "574233135500492810", str(message.guild.owner.id)]:
                    pass
                else:
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
                    with open("./suggestions.json", "w") as f:
                        json.dump(channels, f)
                    try:
                        await message.delete()
                    except:
                        pass


def setup(client):
    client.add_cog(OnMessage(client))
