import json
from nextcord.ext import commands
import nextcord
import pymongo


class Ticket(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command()
    async def ticket(self, ctx):
        client = pymongo.MongoClient(
            f"mongodb+srv://{os.environ['info']}@cluster0.o0xc5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        cluster = client["Guardzilla"]
        tickets = cluster["tickets"]
        ticket = tickets.find_one({"_id": 0})
        if not ticket:
            tickets.insert_one({"_id": 0})
            ticket = tickets.find_one({"_id": 0})
        if str(ctx.guild.id) not in ticket:
            ticket.update({str(ctx.guild.id): []})

        try:
            category = nextcord.utils.get(
                ctx.guild.categories, id=int(ticket[str(ctx.guild.id)][0]))
            if category:
                ticket[str(ctx.guild.id)][0] = str(category.id)
            if not category:
                raise ValueError
        except:
            category = nextcord.utils.get(
                ctx.guild.categories, name='tickets')
            if category:
                try:
                    ticket[str(ctx.guild.id)][0] = str(category.id)
                except IndexError:
                    ticket[str(ctx.guild.id)].append(str(category.id))
            if not category:
                category = await ctx.guild.create_category("tickets", reason=None)
                try:
                    ticket[str(ctx.guild.id)][0] = str(category.id)
                except:
                    ticket[str(ctx.guild.id)].append(str(category.id))
            if not ticket[str(ctx.guild.id)]:
                ticket[str(ctx.guild.id)].append(str(category.id))

        if len(ticket[str(ctx.guild.id)]) == 1:
            role = await ctx.guild.create_role(name="ticket manager")
            ticket[str(ctx.guild.id)].append(str(role.id))
        else:
            role = nextcord.utils.get(
                ctx.guild.roles, id=int(ticket[str(ctx.guild.id)][1]))
            if not role:
                role = nextcord.utils.get(
                    ctx.guild.roles, name="ticket manager")
                if role:
                    ticket[str(ctx.guild.id)][1] = str(role.id)
                elif not role:
                    role = await ctx.guild.create_role(name="ticket manager")
                    try:
                        ticket[str(ctx.guild.id)][1] = str(role.id)
                    except:
                        ticket[str(ctx.guild.id)][1].append(str(role.id))

        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False, send_messages=False),
            ctx.guild.me: nextcord.PermissionOverwrite(
                read_messages=True, send_messages=True),
            ctx.author: nextcord.PermissionOverwrite(
                read_messages=True, send_messages=True),
            role: nextcord.PermissionOverwrite(
                read_messages=True, send_messages=True)
        }
        if len(ticket[str(ctx.guild.id)]) <= 2:
            channel = await ctx.guild.create_text_channel(f"{ctx.author.name}'s ticket", category=category, overwrites=overwrites)
            ticket[str(ctx.guild.id)].append(
                {str(ctx.author.id): [str(channel.id)]})
            await ctx.send(f"New ticket created {channel.mention} | {channel.id}")
            await channel.send("Ticket created.")
        else:
            try:
                if str(ctx.author.id) in ticket[str(ctx.guild.id)][2]:
                    channel = await ctx.guild.fetch_channel(
                        ticket[str(ctx.guild.id)][2][str(ctx.author.id)][0])
                    await ctx.send(f"You already have one {channel.mention} | {channel.id}")
                else:
                    channel = await ctx.guild.create_text_channel(f"{ctx.author.name}'s ticket", category=category, overwrites=overwrites)
                    ticket[str(ctx.guild.id)][2].update(
                        {str(ctx.author.id): [str(channel.id)]})
                    await ctx.message.send(f"New ticket created {channel.mention} | {channel.id}")
                    await channel.send("Ticket created.")
            except:
                channel = await ctx.guild.create_text_channel(f"{ctx.author.name}'s ticket", category=category, overwrites=overwrites)
                ticket[str(ctx.guild.id)][0] = str(category.id)
                ticket[str(ctx.guild.id)][1] = str(role.id)
                ticket[str(ctx.guild.id)][2] = {
                    str(ctx.author.id): [str(channel.id)]}
                await ctx.send(f"New ticket created {channel.mention} | {channel.id}")
        tickets.delete_one({"_id": 0})
        tickets.insert_one(ticket)


def setup(client):
    client.add_cog(Ticket(client))
