import os
import discord
from discord.ext import commands
import openai
import requests
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

bot = commands.Bot(command_prefix="!", intents=intents)

async def chatgpt_query(prompt):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that provides videogame info and advice."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 450,
        "temperature": 0.8,
    }
    response = requests.post(chatgpt_url, json=data, headers=headers)
    response_json = response.json()
    if "choices" in response_json:
        answer = response_json["choices"][0]["message"]["content"].strip()
    else:
        answer = "I'm sorry, I couldn't generate an answer. Please try again later."
    return answer


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.command(name="info", help="Ask advice, strategy, information for any game")
async def info(ctx, *, question):
    answer = await chatgpt_query(question)
    await ctx.send(answer)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Unknown command. Please use the correct command prefix. For example: `!info <your_question>`.")


# Run the bot
bot.run(DISCORD_TOKEN)
