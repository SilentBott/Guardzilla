#the modules i'll use
from nextcord.ext import commands
import pymongo
from os import environ as getenv

class AddBadWords(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.has_permissions(send_messages=True, manage_messages=True)
    @commands.command(name="add-bad-words",
                      aliases=[
                          "add-bad-word", "addbadwords", "addbadword",
                          'add_bad_words', "add_bad_word"
                      ])
    async def addbadwords(self, ctx, *, new_words):
      #connecting to MongoDB server
      db = pymongo.MongoClient(getenv["mongoDBclient"])[str(ctx.message.guild.id)]
      #getting the badwords from the server
      blockedwords = db["blockedwords"]
      data = blockedwords.find_one({"_id": 0})
      #checking if the server id in and adding it if not
      if not data:
          blockedwords.insert_one({"_id": 0, str(ctx.guild.id): [0, []]})
          data = blockedwords.find_one({"_id": 0})
      if str(ctx.guild.id) not in data:
          blockedwords.insert_one({"_id": 0, str(ctx.guild.id): [0, []]})
          data = blockedwords.find_one({"_id": 0})
      #defining the variables i'll use
      words, added_blocked = [], []
      #formatting the text admin send
      for i in range(len(str(new_words).split('"')) // 2):
          words.append(str(new_words).split('"')[i * 2 + 1])
      #checking to not duplicate any word
      for bad_word in words:
          if bad_word not in data[str(ctx.message.guild.id)][1]:
              if bad_word:
                  data[str(ctx.message.guild.id)][1].append(bad_word)
                  added_blocked.append(bad_word)
      # inserting the new data in the mongoDB database
      blockedwords.delete_one({"_id": 0})
      blockedwords.insert_one(data)

      # checking if there is any new words to send to the user if there, otherwise tell the user
      if bool(added_blocked):
          await ctx.send(f"New bad words:\n" +
                         ' | '.join([f"`{x}`"
                                     for x in added_blocked]) + "\nadded!!",
                         delete_after=8)
      else:
          await ctx.send(f"no bad words added.", delete_after=8)

# make the file as cog
def setup(client):
    client.add_cog(AddBadWords(client))
