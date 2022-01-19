import json
from nextcord.ext import commands
import nextcord


class Ticket(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.command()
    async def ticket(self, ctx):
        with open("./tickets.json", ) as f:
            tickets = json.loads(f.read())

        if str(ctx.guild.id) not in tickets:
            tickets.update(
                {str(ctx.guild.id): []})
        try:
            category = nextcord.utils.get(
                ctx.guild.categories, id=int(tickets[str(ctx.guild.id)][0]))
            if category:
                tickets[str(ctx.guild.id)][0] = str(category.id)
            if not category:
                raise ValueError
        except:
            category = nextcord.utils.get(
                ctx.guild.categories, name='tickets')
            if category:
                tickets[str(ctx.guild.id)][0] = str(category.id)
            if not category:
                category = await ctx.guild.create_category("tickets", reason=None)
                try:
                    tickets[str(ctx.guild.id)][0] = str(category.id)
                except:
                    tickets[str(ctx.guild.id)].append(str(category.id))
            if not tickets[str(ctx.guild.id)]:
                tickets[str(ctx.guild.id)].append(str(category.id))

        if len(tickets[str(ctx.guild.id)]) == 1:
            role = await ctx.guild.create_role(name="ticket manager")
            tickets[str(ctx.guild.id)].append(str(role.id))
        else:
            role = nextcord.utils.get(
                ctx.guild.roles, id=int(tickets[str(ctx.guild.id)][1]))
            if not role:
                role = nextcord.utils.get(
                    ctx.guild.roles, name="ticket manager")
                if role:
                    tickets[str(ctx.guild.id)][1] = str(role.id)
                elif not role:
                    role = await ctx.guild.create_role(name="ticket manager")
                    try:
                        tickets[str(ctx.guild.id)][1] = str(role.id)
                    except:
                        tickets[str(ctx.guild.id)][1].append(str(role.id))

        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False, send_messages=False),
            ctx.guild.me: nextcord.PermissionOverwrite(
                read_messages=True, send_messages=True),
            ctx.author: nextcord.PermissionOverwrite(
                read_messages=True, send_messages=True),
            role: nextcord.PermissionOverwrite(
                read_messages=True, send_messages=True)
        }
        if len(tickets[str(ctx.guild.id)]) <= 2:
            channel = await ctx.guild.create_text_channel(f"{ctx.author.name}'s ticket", category=category, overwrites=overwrites)
            tickets[str(ctx.guild.id)].append(
                {str(ctx.author.id): [str(channel.id)]})
            await ctx.send(f"New ticket created {channel.mention} | {channel.id}")
            await channel.send("Hiiiii")
        else:
            try:
                if str(ctx.author.id) in tickets[str(ctx.guild.id)][2]:
                    channel = await ctx.guild.fetch_channel(
                        tickets[str(ctx.guild.id)][2][str(ctx.author.id)][0])
                    await ctx.send(f"You already have one {channel.mention} | {channel.id}")
                else:
                    channel = await ctx.guild.create_text_channel(f"{ctx.author.name}'s ticket", category=category, overwrites=overwrites)
                    tickets[str(ctx.guild.id)][2].update(
                        {str(ctx.author.id): [str(channel.id)]})
                    await ctx.message.send(f"New ticket created {channel.mention} | {channel.id}")
                    await channel.send("Hiiiii")
            except:
                channel = await ctx.guild.create_text_channel(f"{ctx.author.name}'s ticket", category=category, overwrites=overwrites)
                tickets[str(ctx.guild.id)][0] = str(category.id)
                tickets[str(ctx.guild.id)][1] = str(role.id)
                tickets[str(ctx.guild.id)][2] = {
                    str(ctx.author.id): [str(channel.id)]}
                await ctx.send(f"New ticket created {channel.mention} | {channel.id}")
        with open("./tickets.json", "w") as f:
            json.dump(tickets, f)


def setup(client):
    client.add_cog(Ticket(client))
