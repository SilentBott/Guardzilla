from nextcord.ext import commands
import json


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="chat-filter")
    async def chatfilter(self, ctx, allowed):
        with open("./blockedWords.json", ) as f:
            r = json.loads(f.read())
        is_allowed = r[str(ctx.guild.id)][0]
        allowed = allowed[0].lower()
        if allowed in ["d", "a", '1', '0', 't', 'f']:
            if allowed in ["d", 'f', '0']:
                allowed = 0
            elif allowed in ["a", 't', '1']:
                allowed = 1
            if allowed == is_allowed:
                await ctx.reply(f"The chat filter is already set to: {'allowed' if allowed else 'disabled'} mode")
            else:
                with open("./blockedWords.json", "w") as f:
                    r[str(ctx.guild.id)][0] = allowed
                    json.dump(r, f)
                await ctx.reply(f"The chat filter set to: {'allowed' if allowed else 'disabled'} mode")
        else:
            await ctx.reply("")


def setup(client):
    client.add_cog(Admin(client))
