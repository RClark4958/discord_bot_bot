import os
import discord
from discord.ext import commands
import openai
import aiohttp  # <-- Imported for async HTTP
from dotenv import load_dotenv

# Load the Discord bot token and OpenAI API key from environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up the ChatGPT API client
chatgpt_url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# Set up the Discord bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def chatgpt_query(prompt):
    async with aiohttp.ClientSession() as session:
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a helpful and cheery devops and software engineering expert."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 8000,
            "temperature": 0.8,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        async with session.post(chatgpt_url, json=data, headers=headers) as response:
            response_json = await response.json()
            if "choices" in response_json:
                answer = response_json["choices"][0]["message"]["content"].strip()
            else:
                answer = "I'm sorry, I couldn't generate an answer. Please try again later"
            return answer

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.command(name="info", help="Ask advice, strategy, information for any game")
async def info(ctx, *, question):
    answer = await chatgpt_query(question)
    
    # Split answer into chunks for Discord's 2000 character limit
    for chunk in [answer[i:i + 1990] for i in range(0, len(answer), 1990)]:
        await ctx.send(chunk)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command. Please use the correct command prefix. For example: `!info <your_question>`.")

# Run the bot
bot.run(DISCORD_TOKEN)
