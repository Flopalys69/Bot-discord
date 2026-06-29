import discord
from discord.ext import commands
import time
import json

XP_FILE = "../xp.json"

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

cooldowns = {}

LEVEL_ROLES = {
    5: "Gamer",
    10: "Pro",
    20: "Legend"
}

class Levels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        user = str(message.author.id)

        now = time.time()

        if user in cooldowns and now - cooldowns[user] < 30:
            return

        cooldowns[user] = now

        if user not in xp:
            xp[user] = {"xp": 0, "level": 0}

        xp[user]["xp"] += 5

        new_level = xp[user]["xp"] // 50

        if new_level > xp[user]["level"]:
            xp[user]["level"] = new_level

            await message.channel.send(
                f"🎉 {message.author.mention} passe **niveau {new_level}** !"
            )

            if new_level in LEVEL_ROLES:
                role_name = LEVEL_ROLES[new_level]
                role = discord.utils.get(message.guild.roles, name=role_name)

                if role:
                    await message.author.add_roles(role)
                    await message.channel.send(
                        f"🎖 {message.author.mention} a reçu le rôle **{role_name}** !"
                    )

        save_xp(xp)

    @commands.command()
    async def rank(self, ctx):

        user = str(ctx.author.id)

        if user not in xp:
            return await ctx.send("Aucun XP.")

        user_xp = xp[user]["xp"]
        level = xp[user]["level"]

        next_level_xp = (level + 1) * 50

        progress = int((user_xp % 50) / 5)

        bar = "█" * progress + "░" * (10 - progress)

        await ctx.send(
            f"⭐ {ctx.author.name}\n"
            f"Niveau : **{level}**\n"
            f"XP : **{user_xp} / {next_level_xp}**\n"
            f"{bar}"
        )

async def setup(bot):
    await bot.add_cog(Levels(bot))