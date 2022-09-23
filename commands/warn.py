from nextcord.ext import commands
import nextcord
from datetime import datetime, timezone
import pymongo
from os import environ as getenv


class Warn(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command()
    async def warn(self, ctx, member, *, reason=None):
        if reason is None:
            reason = "No Reason"
        try:
            member = str(int(member))
        except ValueError:
            member = member.split("<@")[1].split(">")[0].replace("!", "")
        member = await ctx.guild.fetch_member(member)
        if str(member.id) == str(ctx.author.id):
            embed = nextcord.Embed(color=0x00ff00,
                                   title="You cannot warn yourself")
            await ctx.send(embed=embed)
            return
        embed = nextcord.Embed(color=0x00ff00)
        db = pymongo.MongoClient(getenv["mongoDBclient"])[ctx.message.guild.id]
        warns = db["warns"]
        warnings = warns.find_one({"_id": 0})

        time = str(datetime.utcnow().replace(
            tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))

        if not warnings:
            warns.insert_one({"_id": 0})
            warnings = warns.find_one({"_id": 0})
        if str(ctx.guild.id) in warnings:
            if str(member.id) in warnings[str(ctx.guild.id)]:
                warnings[str(ctx.guild.id)][str(member.id)].append(
                    [time, str(ctx.author.id), reason])
            else:
                warnings[str(ctx.guild.id)].update(
                    {str(member.id): [[time, str(ctx.author.id), reason]]})
        else:
            warnings.update({str(ctx.guild.id): {}})
            warnings[str(ctx.guild.id)].update({str(member.id): []})
            warnings[str(ctx.guild.id)][str(member.id)].append(
                [time, str(ctx.author.id), reason])
        warns.delete_one({"_id": 0})
        warns.insert_one(warnings)

        embed = nextcord.Embed(
            title=
            f"The member {member.display_name} | {member.id}\nwarned Reason:\n``` {reason} ```",
            color=0x00ff00)
        embed.set_footer(
            text=f"Warned by: {ctx.author.name} | {ctx.author.id}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Warn(client))
