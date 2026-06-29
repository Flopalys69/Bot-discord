import discord
from discord.ext import commands
from datetime import timedelta
import config

def is_moderator(user_id):
    return user_id == config.OWNER_ID or user_id in config.MOD_IDS


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def mute(self, ctx, duration: int, member: discord.Member):

        if not is_moderator(ctx.author.id):
            return await ctx.send("❌ Pas la permission.")

        if member.id == config.OWNER_ID:
            return await ctx.send("❌ Impossible de mute le propriétaire.")

        await member.timeout(timedelta(seconds=duration))

        await ctx.send(f"🔇 {member.mention} mute pendant {duration} sec.")


    @commands.command()
    async def unmute(self, ctx, member: discord.Member):

        if not is_moderator(ctx.author.id):
            return await ctx.send("❌ Pas la permission.")

        await member.timeout(None)

        await ctx.send(f"🔊 {member.mention} unmute.")


    @commands.command()
    async def clear(self, ctx, amount: int):

        if not is_moderator(ctx.author.id):
            return await ctx.send("❌ Pas la permission.")

        await ctx.channel.purge(limit=amount + 1)

        await ctx.send(f"🧹 {amount} messages supprimés.", delete_after=5)


    @commands.command()
    async def clearuser(self, ctx, member: discord.Member, amount: int):

        if not is_moderator(ctx.author.id):
            return await ctx.send("❌ Pas la permission.")

        if member.id == config.OWNER_ID:
            return await ctx.send("❌ Impossible de supprimer ses messages.")

        deleted = 0

        async for message in ctx.channel.history(limit=200):

            if message.author == member:
                await message.delete()
                deleted += 1

                if deleted >= amount:
                    break

        await ctx.send(
            f"🧹 {deleted} messages supprimés de {member.mention}.",
            delete_after=5
        )

async def setup(bot):
    await bot.add_cog(Moderation(bot))