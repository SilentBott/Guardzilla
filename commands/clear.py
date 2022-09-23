# importing all required modules
from nextcord.ext import commands


class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="clear")
    async def clear(self, ctx, num: int, member=None, channel=None):
        #check if no channel selected
        if channel == None:
            #make current one as default one
            channel = ctx.channel
        else:
            #get the selected channel
            if "#" in channel:
                channel = await ctx.guild.fetch_channel(
                    channel.replace("<#", '').replace(">", ""))
            else:
                try:
                    channel = await ctx.guild.fetch_channel(channel)
                except:
                    if channel.lower()[0:3] == "all":
                        channel = "all"
                    else:
                        channel = ctx.channel
        #get the member who the bot'll delete his messages
        if member != None:
            try:
                member = str(int(member))
            except ValueError:
                member = member.split("<@")[1].split(">")[0].replace("!", "")
            member = await ctx.guild.fetch_member(member)
        # if admin put above the highest range
        if num >= 100:
            await ctx.send(
                f"you cannot put number above 100\nWe will make it 100 for you",
                delete_after=3)
            num = 100
        # if the number range is correct
        if num > 0:
            #if admin chose member
            if member != None:
                #make the channels the bot'll delete from
                channels = [channel]
                if channel == 'all':
                    channels = ctx.guild.text_channels
                for channel in channels:
                    #get the messages log of the member
                    messages = await channel.history(limit=100).flatten()
                    deleted = 0
                    for msg in messages:
                        #delete messages if its from the member
                        if str(msg.author.id) == str(member.id):
                            await msg.delete()
                            deleted += 1
                        if deleted >= num:
                            break
                    # get the number of deleted messages
                    await ctx.send(
                        f"{deleted}message deleted of the user {member} in {channel.mention}",
                        delete_after=8)
            else:
                #delete messages
                nu = await channel.purge(limit=num + 1)
                await ctx.send(f"{len(nu)-1}message deleted", delete_after=5)
        #check if there is minus number
        elif num <= 0:
            await ctx.send(f"You cannot put minus in clear mode.",
                           delete_after=5)


# add command as cog
def setup(client):
    client.add_cog(Clear(client))
