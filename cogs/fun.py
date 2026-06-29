import discord
from discord.ext import commands
import random

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def dice(self, ctx):
        await ctx.send(f"🎲 {random.randint(1,6)}")


    @commands.command()
    async def coin(self, ctx):
        await ctx.send(random.choice(["Pile", "Face"]))


    @commands.command()
    async def rps(self, ctx, choix):

        choix_bot = random.choice(["pierre","feuille","ciseaux"])

        await ctx.send(f"🤖 J'ai choisi **{choix_bot}**")


    @commands.command()
    async def roast(self, ctx, member: discord.Member):

        roasts = [
            #"Même Google ne trouve pas ton intelligence.",
            #"Tu es la raison pour laquelle il y a des instructions sur le shampooing.",
            #"Ton cerveau est en mode économie d'énergie.",
            "NTM",
            #"Retourne Manger des nems",
            #"T nul a Valorant reste FER",
            "ta mere aurait du t'avorter",
            "TA PA DE VI,PA DAMI,PA DPARENT"

        ]

        await ctx.send(f"{member.mention} {random.choice(roasts)}")


    @commands.command()
    async def love(self, ctx, m1: discord.Member, m2: discord.Member):

        score = random.randint(0,100)

        await ctx.send(f"❤️ Compatibilité : **{score}%**")


async def setup(bot):
    await bot.add_cog(Fun(bot))