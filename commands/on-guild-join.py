from nextcord.ext import commands
import json


class OnGuildJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("./prefix.json", ) as f:
            read = json.loads(f.read())
        if str(guild.id) in read:
            pass
        else:
            read.update({str(guild.id): "!"})
            with open("./prefix.json", "w") as f:
                json.dump(read, f)

        with open("./blockedWords.json", ) as f:
            read = json.loads(f.read())
        if str(guild.id) in read:
            pass
        else:
            read.update({str(guild.id): [0, []]})
            with open("./blockedWords.json", "w") as f:
                json.dump(read, f)


def setup(client):
    client.add_cog(OnGuildJoin(client))
