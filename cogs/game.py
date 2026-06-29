import discord
from discord.ext import commands
import random

class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def rate(self, ctx, *, thing):

        score = random.randint(0,100)

        await ctx.send(f"⭐ Je donne **{score}/100** pour **{thing}**")


    @commands.command()
    async def eightball(self, ctx, *, question):

        responses = [
            "Oui",
            "Non",
            "Peut-être",
            "Très probable",
            "Très improbable"
        ]

        await ctx.send(f"🎱 {random.choice(responses)}")


    @commands.command()
    async def meme(self, ctx):

        memes = [
            "https://i.imgur.com/w3duR07.png",
            "https://i.imgur.com/9v3P2cC.png",
            "https://i.imgur.com/F3p7K9R.png"
        ]

        await ctx.send(random.choice(memes))


async def setup(bot):
    await bot.add_cog(Games(bot))