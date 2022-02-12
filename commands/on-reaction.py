from nextcord.ext import commands
import json
from nextcord.utils import get
import nextcord
import pymongo
import os


class OnReaction(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        reaction_roles = cluster["reaction_roles"]
        r = reaction_roles.find_one({"_id": 0})
        if not r:
            reaction_roles.insert_one({"_id": 0})
            r = reaction_roles.find_one({"_id": 0})
        if str(payload.guild_id) not in r:
            r.update({str(payload.guild_id): ""})
            reaction_roles.delete_one({"_id": 0})
            reaction_roles.insert_one(r)
            r = reaction_roles.find_one({"_id": 0})

        if str(payload.message_id) in r:
            emoji = self.client.get_emoji(r[str(payload.message_id)][0])
            guild = self.client.get_guild(payload.guild_id)
            role = get(guild.roles, id=r[str(payload.message_id)][1])
            if payload.emoji.id == emoji.id:
                await payload.member.add_roles(role, reason="None")

        suggestions = cluster["suggestions"]
        l = suggestions.find_one({"_id": 0})
        if not l:
            suggestions.insert_one({"_id": 0})
            l = prefix.find_one({"_id": 0})
        if str(payload.guild_id) not in l:
            suggestions.insert_one({"_id": 0})
            l = prefix.find_one({"_id": 0})

        if str(payload.guild_id) in l:
            if str(payload.channel_id) == l[str(payload.guild_id)][0]:
                if str(payload.message_id) in l[str(payload.guild_id)][1][0]:
                    lock_k = 932702977976836136
                    unlock_k = 932702978031374457
                    if payload.emoji.id in [lock_k, unlock_k]:
                        channel = self.client.get_channel(payload.channel_id)
                        message = await channel.fetch_message(payload.message_id)
                        check_l = self.client.get_emoji(lock_k)
                        uncheck_l = self.client.get_emoji(unlock_k)
                        guild = self.client.get_guild(payload.guild_id)
                        member = await guild.fetch_member(l[str(payload.guild_id)][1][0][str(payload.message_id)][1])
                        avatar_url = member.avatar.url

                        likes, dislikes = get(message.reactions, emoji=check_l).count, get(
                            message.reactions, emoji=uncheck_l).count
                        embed = nextcord.Embed(description=l[str(payload.guild_id)][1][0][str(payload.message_id)][0],
                                               color=0x00ff00)
                        embed.set_author(
                            name=f"{member} Suggestion", icon_url=avatar_url)
                        embed.set_thumbnail(url=avatar_url)
                        embed.add_field(name="Up votes:",
                                        value=f"{likes-1} Vote")
                        embed.add_field(name="Down votes:",
                                        value=f"{dislikes-1} Vote")
                        if self.client.user.avatar:
                            embed.set_footer(text="Wants to send suggestion? Simply type in this channel!",
                                             icon_url=self.client.user.avatar.url)
                        else:
                            embed.set_footer(
                                text="Wants to send suggestion? Simply type in this channel!")

                        await message.edit(embed=embed)

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        reaction_roles = cluster["reaction_roles"]
        r = reaction_roles.find_one({"_id": 0})
        if not r or str(payload.guild_id) not in r:
            reaction_roles.insert_one({"_id": 0})
            r = prefix.find_one({"_id": 0})

        if str(payload.message_id) in r:
            emoji = self.client.get_emoji(r[str(payload.message_id)][0])
            guild = self.client.get_guild(payload.guild_id)
            role = get(guild.roles, id=r[str(payload.message_id)][1])
            if payload.emoji.id == emoji.id:
                member = await guild.fetch_member(payload.user_id)
                if member.bot:
                    return
                await member.remove_roles(role)
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        suggestions = cluster["suggestions"]
        l = suggestions.find_one({"_id": 0})
        if not l:
            suggestions.insert_one({"_id": 0})
            l = prefix.find_one({"_id": 0})
        if str(payload.guild_id) not in l:
            suggestions.insert_one({"_id": 0})
            l = prefix.find_one({"_id": 0})

        if str(payload.guild_id) in l:
            if str(payload.channel_id) == l[str(payload.guild_id)][0]:
                if str(payload.message_id) in l[str(payload.guild_id)][1][0]:
                    lock_k = 932702977976836136
                    unlock_k = 932702978031374457
                    if payload.emoji.id in [lock_k, unlock_k]:
                        channel = self.client.get_channel(payload.channel_id)
                        message = await channel.fetch_message(payload.message_id)
                        check_l = self.client.get_emoji(lock_k)
                        uncheck_l = self.client.get_emoji(unlock_k)
                        guild = self.client.get_guild(payload.guild_id)
                        member = await guild.fetch_member(l[str(payload.guild_id)][1][0][str(payload.message_id)][1])
                        avatar_url = member.avatar.url

                        likes, dislikes = get(message.reactions, emoji=check_l).count, get(
                            message.reactions, emoji=uncheck_l).count
                        embed = nextcord.Embed(description=l[str(payload.guild_id)][1][0][str(payload.message_id)][0],
                                               color=0x00ff00)
                        embed.set_author(
                            name=f"{member} Suggestion", icon_url=avatar_url)
                        embed.set_thumbnail(url=avatar_url)
                        embed.add_field(name="Up votes:",
                                        value=f"{likes-1} Vote")
                        embed.add_field(name="Down votes:",
                                        value=f"{dislikes-1} Vote")
                        if self.client.user.avatar:
                            embed.set_footer(text="Wants to send suggestion? Simply type in this channel!",
                                             icon_url=self.client.user.avatar.url)
                        else:
                            embed.set_footer(
                                text="Wants to send suggestion? Simply type in this channel!")
                        await message.edit(embed=embed)


def setup(client):
    client.add_cog(OnReaction(client))
