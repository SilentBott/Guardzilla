from nextcord.ext import commands
import pymongo
from os import environ as getenv


class chatFilter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="chat-filter")
    async def chatFilter(self, ctx, allowed):
        #connecting to MogoDB server
        db = pymongo.MongoClient(getenv["mongoDBclient"])[str(
            ctx.message.guild.id)]
        blockedwords = db["blockedwords"]
        #find it or create one in db if there is not
        try:
            isAllowed = blockedwords.find_one({"_id": 0})
            isAllowed["allowed"]
        except KeyError:
            isAllowed = 0
        if not isAllowed["allowed"]:
            blockedwords.insert_one({"_id": 0, "allowed": 0, "words": []})
            isAllowed = blockedwords.find_one({"_id": 0})
        # check if all things is o k
        allowed = allowed[0].lower()
        if allowed in ["d", "a", '1', '0', 't', 'f']:
            if allowed in "df0":
                allowed = 0
            elif allowed in "at1":
                allowed = 1
            if allowed == isAllowed["allowed"]:
                #send if its already allowed/disabled
                await ctx.reply(
                    f"The chat filter is already set to: {'allowed' if allowed else 'disabled'} mode"
                )
            else:
                # changing everythings in the db
                isAllowed["alllowed"] = allowed
                blockedwords.delete_one({"_id": 0})
                blockedwords.insert_one(isAllowed)
                await ctx.reply(
                    f"The chat filter set to: {'allowed' if allowed else 'disabled'} mode"
                )
        else:
            await ctx.reply("please specific the wanted state(true/false)")


# add the command as cog
def setup(client):
    client.add_cog(chatFilter(client))
