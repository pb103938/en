import discord
import os
import requests
import json
import random
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "upset", "unhappy", "not happy", "angry", "miserable","feeling down"]

starter_encouragements = [
"cheer up!", 
"it's ok.", 
"don't listen to the bully, his words are wrong."
]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('i%help'))
    print('logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith('i%inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if message.content.startswith('i%help'):
        await message.channel.send(
            '(use i%help commands for commands). prefix: i%; version: 2.3.5'
        )

    if message.content.startswith('^botservers'):
         await message.channel.send( f"I'm in {len(client.guilds)} servers!")

    if message.content.startswith('i%help commands'):
        await message.channel.send(
            'commands:  (i%help. use: displays some basic commands. ), (i%inspire. use: sends an encouraging message to your server) (i%invite. use: use this command to invite the bot to your server or get invited to the bots server) (i%update. use: sends you a message with information about the most recent update.)')

    if message.content.startswith('i%invite'):
        await message.channel.send(
            'our server: https://discord.gg/brR4DMPUb5. invite the bot: https://discord.com/api/oauth2/authorize?client_id=791768754518228992&permissions=2147862592&scope=bot')

    if message.content.startswith('i%update'):
        await message.channel.send(
            'Removed word "mad" from response list, meaning bot will no longer respond to messages containing made or mad. If you know how to fix this please DM Pb103938#0572 or join our server, https://discord.gg/brR4DMPUb5 and go to the suggestions channel and post it there. bot runs on discord.py.'
        )
    
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))

keep_alive()
token = os.getenv('TOKEN')
client.run(token)
client.run(os.getenv('TOKEN'))