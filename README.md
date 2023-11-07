# discord_bot

This bot uses the gpt-4-turbo-preview model to respond to user prompts with help for writing code and configuring devops. The bot is set up to maintain context with an individual user. The session can be reset at any time with !reset. Signal the bot by using !info at the beginning of a request. At this time the bot stores data in memory and will not retain conversations after a container restart.

## Implementation

Using this bot requires a openai api key (costs money) and a registered discord application (free). 

## notes

Create a '.env' file and set
`DISCORD_TOKEN=<your_token_value>` and `OPENAI_API_KEY=<your_key_value>`

The filepath for the app folder in docker-compose.yml can be adjusted. Helpful if using a docker-compose.yml that spins up several containers.