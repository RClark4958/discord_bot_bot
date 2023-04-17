# discord_bot

This bot uses the gpt-3.5-turbo model to respond to user prompts with information and advice about specific games.

## Implementation

Using this bot requires a openai api key (costs money) and a registered discord application (free).

## notes

Create a '.env' file and set
`DISCORD_TOKEN=<your_token_value>` and `OPENAI_API_KEY=<your_key_value>`

The filepath for the app folder in docker-compose.yml can be adjusted. Helpful if using a docker-compose.yml that spins up several containers.