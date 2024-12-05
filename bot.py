import discord
from discord.ext import commands
from dotenv import load_dotenv
from ec2_metadata import ec2_metadata
import random
import os

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize bot with command prefix "!"
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot ready event
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# Command: Status
@bot.command(name="status")
async def status(ctx):
    try:
        # Fetch EC2 Metadata
        public_ip = ec2_metadata.public_ipv4
        region = ec2_metadata.region
        availability_zone = ec2_metadata.availability_zone

        # Send metadata to Discord channel
        await ctx.send(
            f"EC2 Instance Metadata:\n"
            f"- Public IP: {public_ip}\n"
            f"- Region: {region}\n"
            f"- Availability Zone: {availability_zone}"
        )
    except Exception as e:
        await ctx.send(f"Error fetching metadata: {str(e)}")

# Command: Joke
@bot.command(name="joke")
async def joke(ctx):
    jokes = [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call fake spaghetti? An impasta.",
        "Why don’t skeletons fight each other? They don’t have the guts.",
    ]
    await ctx.send(random.choice(jokes))

@bot.event
async def on_message(message):
    # Log messages the bot receives
    print(f"Message from {message.author}: {message.content}")

    # Process commands if the bot is mentioned
    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
