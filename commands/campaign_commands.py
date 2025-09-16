import psycopg2
from discord.ext import commands
from Campaign import Campaign
import os

database_url = os.getenv("DATABASE_URL")

class CampaignCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create_campaign")
    async def create_campaign(self, ctx, *, campaign_name: str):
        """Create a new campaign where the user is the DM."""
        dm_id = ctx.author.id
        try:
            conn = psycopg2.connect(database_url)
            campaign_id = Campaign.create_campaign(conn, campaign_name, dm_id)
            await ctx.send(f"Campaign '{campaign_name}' created successfully with ID {campaign_id}, and you are the DM!")
        except Exception as e:
            await ctx.send(f"An error occurred while creating the campaign: {e}")
        finally:
            conn.close()

    @commands.command(name="list_campaigns")
    async def list_campaigns(self, ctx):
        """List all campaigns where the user is the DM."""
        dm_id = ctx.author.id
        try:
            conn = psycopg2.connect(database_url)
            with conn.cursor() as cur:
                cur.execute("SELECT id, name FROM campaigns WHERE dm_id = %s;", (dm_id,))
                campaigns = cur.fetchall()
                if campaigns:
                    response = "Here are the campaigns you are DMing:\n"
                    response += "\n".join([f"ID: {campaign[0]}, Name: {campaign[1]}" for campaign in campaigns])
                else:
                    response = "You are not DMing any campaigns."
            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"An error occurred while retrieving your campaigns: {e}")
        finally:
            conn.close()

async def setup(bot):
    await bot.add_cog(CampaignCommands(bot))