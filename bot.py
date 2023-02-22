from api import Character
import discord

char_id = ""
char_token = ""
disc_token = ""
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents = intents)
api = Character(char_token, char_id)

@bot.event
async def on_message(message):
	if message.author != bot.user:
		async with message.channel.typing():
			await message.channel.send(api.stream(message.content))

@bot.command()
async def reset(context):
	await context.defer()
	await context.respond(api.create())
	
@bot.command()
async def change(context, id: str):
	await context.defer()
	await context.respond(api.setup(id))

bot.run(disc_token)