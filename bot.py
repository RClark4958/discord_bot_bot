import os
import discord
from discord.ext import commands
import openai
import aiohttp
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

chatgpt_url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Maintain a conversation state for each user
conversation_states = {}

async def chatgpt_query(prompt, user_id):
    # Retrieve the current conversation state for the user if it exists
    conversation_state = conversation_states.get(user_id, [])

    data = {
        "model": "gpt-4-1106-preview",
        "messages": conversation_state + [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4096,
        "temperature": 0.8,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(chatgpt_url, json=data, headers=headers) as response:
            response_json = await response.json()
            if "choices" in response_json:
                # Extract the content of the response
                answer_content = response_json["choices"][0]["message"]["content"].strip()
                # Update the conversation state with the new user and bot messages
                conversation_states[user_id] = conversation_state + [
                    {"role": "user", "content": prompt},
                    {"role": "system", "content": answer_content}
                ]
                return answer_content
            else:
                return "I'm sorry, I couldn't generate an answer. Please try again later."

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.command(name="info", help="Request instruction in writing code, working with infrastructure as code, and configuring cloud resources")
async def info(ctx, *, question):
    # Pass the user ID to maintain context for that user
    answer = await chatgpt_query(question, ctx.author.id)

    # Split answer into chunks for Discord's 2000 character limit
    for chunk in [answer[i:i + 1990] for i in range(0, len(answer), 1990)]:
        await ctx.send(chunk)

@bot.command(name="reset", help="Reset the conversation context for the user.")
async def reset(ctx):
    # Reset the conversation state for the user
    user_id = ctx.author.id
    if user_id in conversation_states:
        del conversation_states[user_id]
        await ctx.send("Your conversation context has been reset.")
    else:
        await ctx.send("You have no conversation to reset.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command. Please use the correct command prefix. For example: !info <your_question>.")

bot.run(DISCORD_TOKEN)
