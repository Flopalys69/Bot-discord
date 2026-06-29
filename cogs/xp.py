import discord
from discord.ext import commands
import json

XP_FILE = "xp.json"


def load_xp():
    try:
        with open(XP_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_xp(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f, indent=4)


xp = load_xp()


class XP(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        user = str(message.author.id)

        if user not in xp:
            xp[user] = {"xp": 0, "level": 0}

        xp[user]["xp"] += 1

        level = xp[user]["xp"] // 50

        if level > xp[user]["level"]:
            xp[user]["level"] = level
            await message.channel.send(
                f"🎉 {message.author.mention} passe **niveau {level}** !"
            )

        save_xp(xp)


    @commands.command()
    async def xp(self, ctx):

        user = str(ctx.author.id)

        if user not in xp:
            return await ctx.send("⭐ XP : 0 | Niveau : 0")

        user_xp = xp[user]["xp"]
        level = xp[user]["level"]

        await ctx.send(
            f"⭐ {ctx.author.mention}\nXP : **{user_xp}**\nNiveau : **{level}**"
        )


    @commands.command()
    async def leaderboard(self, ctx):

        ranking = sorted(
            xp.items(),
            key=lambda x: (x[1]["level"], x[1]["xp"]),  # trie par niveau, puis XP
            reverse=True
        )[:10]
        msg = "🏆 **Leaderboard XP**\n\n"

        for i, (user_id, data) in enumerate(ranking):

            member = ctx.guild.get_member(int(user_id))

            if not member:
                continue

            score = data["xp"]
            level = data["level"]

            msg += f"{i+1}. {member.name} — Niveau {level} ({score} XP)\n"

        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(XP(bot))