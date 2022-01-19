import json
from nextcord.ext import commands
import nextcord
msgs = {}


class ReactionRole(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.command(name="reaction-role")
    async def reaction_role(self, ctx, msg_id: int, emoji: nextcord.Emoji, role: nextcord.Role):
        global msgs
        if ctx.author.top_role > role or ctx.author.id == ctx.guild.owner.id:
            msg = await ctx.fetch_message(msg_id)
            await msg.add_reaction(emoji=emoji)
            with open("./reaction_roles.json", ) as f:
                r = json.loads(f.read())
            r.update({str(msg_id): [int(emoji.id), int(role.id)]})
            with open("./reaction_roles.json", "w") as f:
                json.dump(r, f)


def setup(client):
    client.add_cog(ReactionRole(client))
