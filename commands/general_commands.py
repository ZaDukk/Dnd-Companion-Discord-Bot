from discord.ext import commands

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        """Respond with a greeting."""
        await ctx.send(f"shut up, {ctx.author.mention}!")

async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))