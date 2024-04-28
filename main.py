import discord
import os
from discord import app_commands, utils
import requests
import json
import random
from keep_alive import keep_alive
from replit import db


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

cmds = app_commands.CommandTree(client)

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

def get_verse():
  response = requests.post("https://dailyverses.net/get/random?language=esv")
  verse = response.text.split(">")
  verse = str(verse).split("<")
  verseText = verse[1].replace("""div class="dailyVerses bibleText"', '""", "")
  verseNo = verse[4].split()
  
  book = verseNo[-2].replace("'", "")
  num = verseNo[-1]

  response = f"""{book.upper()} {num} - {verseText}"""
  
  return response

def is_admin(interaction: discord.Interaction):
  return interaction.user.guild_permissions.administrator

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f'/help in {len(client.guilds)} servers!'))
    await cmds.sync()
    await cmds.sync(guild=discord.Object(id=1082398616649482290))
    print('logged in as {0.user}'.format(client), f"\nServers: {len(client.guilds)} \nDatabases: {len(db)}")

@client.event
async def on_guild_remove(server):

  ids = ["DMs"]

  
  for guild in client.guilds:
    ids.append(str(guild.id))

  for id in db:
    if ids.count(str(id)) == 0:
      del db[str(id)]
      print(f"Successfully deleted data for: {id}.")

  await client.change_presence(
    status=discord.Status.online,
    activity=discord.Game(f'/help in {len(client.guilds)} servers!'))

@client.event
async def on_guild_join(guild):
  await client.change_presence(
    status=discord.Status.online,
    activity=discord.Game(f'/help in {len(client.guilds)} servers!'))

# This example uses topggpy's autopost feature to post guild count to Top.gg every 30 minutes
# as well as the shard count if applicable.

#dbl_token = os.getenv('TOPGG_TOKEN')  # set this to your bot's Top.gg token
#bot.topggpy = topgg.DBLClient(client, dbl_token, autopost=True, post_shard_count=True)


#@client.event
#async def on_autopost_success():
 #   print(

#f"Posted server count ({client.topggpy.guild_count}), shard count ({client.shard_count})"
 #   )

@cmds.command(
  name="help",
  description="sends an embed with some helpful information",
)
async def help_command(interaction: discord.Interaction):
  await interaction.response.defer()
  await interaction.followup.send(embed=discord.Embed(
            title='help',
            description=
            '(use </commands:1081698755218247802> for commands.) version: 1.5.3 \n\n Issue resolved. Bot should run without an issue now.',
            color=5763719).add_field(name="Privacy Policy", value="Click [here](https://docs.google.com/document/d/1HbJcobW_O_P3QIrPcXaXZP3PoaPqvHNGAtPKxiLCsIc/edit?usp=sharing) to view Encourager's Privacy Policy.").add_field(name="Terms of Service", value="Click [here](https://docs.google.com/document/d/1oxim4UQxqzo0bUYICe-uWWo2nU5aFLrqC_LozUKc5fc/edit?usp=sharing) to view Encourager's Terms of Service."))

@cmds.context_menu(
  name="Report Message",
  guild=discord.Object(id=1082398616649482290)
)
async def report_menu(interaction, message: discord.Message):
  channel = utils.get(interaction.guild.text_channels, name="reports")
  await channel.send(embed=discord.Embed(title="Report", description=f"{interaction.user.mention} reported {message.author.mention}{chr(39)}s message. \n\n**Message:**\n{message.content}\n\n**Message link:**\nclick [here]({message.jump_url}) to jump to the message."))
  await interaction.response.send_message("Message reported!", ephemeral=True)

@cmds.command(
  name="report",
  description="Report someone for unruly action.",
  guild=discord.Object(id=1082398616649482290)
)
async def report_command(interaction, user: discord.User, reason: str):
  channel = utils.get(interaction.guild.text_channels, name="reports")
  await channel.send(embed=discord.Embed(title="Report", description=f"{interaction.user.mention} reported {user.mention}. \n\n**Reason:**\n{reason}"))
  await interaction.response.send_message("User reported!", ephemeral=True)


#BEGIN database section

#begin Add class
@app_commands.guild_only()
class Add(app_commands.Group):

  #add sadword command
  @app_commands.command(
    name="sad-word",
    description="lets you add a sad word or phrase which the bot will respond to"
  )
  async def add_sad_word(self, interaction: discord.Interaction, word: str):

    await interaction.response.defer()

    if is_admin(interaction) == True:
      guildId = interaction.guild.id #Gets the guild ID
  
      try: #Tests if that server already has a database section
        db[str(guildId)]
      except: #If not, it creates one
        db[str(guildId)] = {"sad_words": ["sad", "depressed", "upset", "unhappy", "not happy", "angry", "miserable", "feeling down"], "responses": ["cheer up!", "it's ok.", "don't listen to the bully, his words are wrong.", "You know what's good about hitting rock bottom, there's only one way left to go, and that's, up!"], "enabled":True}
        print("Created new database for: ", guildId)
  
      #adds the word
      guildDB = db[str(guildId)]
      sWords = guildDB['sad_words']
      if any(words in word.lower() for words in sWords):
        await interaction.followup.send("You already added this word!", ephemeral=True)
      else:
        sWords.append(word.lower())
        await interaction.followup.send(f"successfully added the word **{word}** to your server's list of sad words!", ephemeral=True)

    else:
      await interaction.followup.send("You must be an admin to use this command!", ephemeral=True)


  #add response command
  @app_commands.command(
    name="response",
    description="lets you add a word or phrase which the bot will respond to sad words with"
  )
  async def add_response(self, interaction: discord.Interaction, word: str):

    await interaction.response.defer()

    if is_admin(interaction) == True:
      guildId = interaction.guild.id #Gets the guild ID
  
      try: #Tests if that server already has a database section
        db[str(guildId)]
      except: #If not, it creates one
        db[str(guildId)] = {"sad_words": ["sad", "depressed", "upset", "unhappy", "not happy", "angry", "miserable", "feeling down"], "responses": ["cheer up!", "it's ok.", "don't listen to the bully, his words are wrong.", "You know what's good about hitting rock bottom, there's only one way left to go, and that's, up!"], "enabled":True}
        print("Created new database for: ", guildId)
  
      #adds the word
      guildDB = db[str(guildId)]
      rWords = guildDB['responses']
  
      if any(words in word.lower() for words in rWords):
        await interaction.followup.send("You already added this word!", ephemeral=True)
      else:
        rWords.append(word.lower())
        await interaction.followup.send(f"successfully added the word **{word}** to your server's list of responses!", ephemeral=True)

    else:
      await interaction.followup.send("You must be an admin to use this command!", ephemeral=True)
    
#End Add class

cmds.add_command(Add()) #Adds Add class commands


#Begin Remove class
@app_commands.guild_only()
class Remove(app_commands.Group):

  #remove sadword command
  @app_commands.command(
    name="sad-word",
    description="lets you remove a sad word or phrase which the bot will respond to"
  )
  async def add_sad_word(self, interaction: discord.Interaction, word: str):

    await interaction.response.defer()

    if is_admin(interaction) == True:
      guildId = interaction.guild.id #Gets the guild ID
  
      try: #Tests if that server already has a database section
        db[str(guildId)]
      except: #If not, it creates one
        db[str(guildId)] = {"sad_words": ["sad", "depressed", "upset", "unhappy", "not happy", "angry", "miserable", "feeling down"], "responses": ["cheer up!", "it's ok.", "don't listen to the bully, his words are wrong.", "You know what's good about hitting rock bottom, there's only one way left to go, and that's, up!"], "enabled":True}
        print("Created new database for: ", guildId)
  
      #removes the word
      guildDB = db[str(guildId)]
      sWords = guildDB['sad_words']
      if not any(words in word.lower() for words in sWords):
        await interaction.followup.send("Word could not be found.", ephemeral=True)
      else:
        sWords.remove(word.lower())
        await interaction.followup.send(f"successfully removed the word **{word}** to your server's list of sad words!", ephemeral=True)

    else:
      await interaction.followup.send("You must be an admin to use this command!", ephemeral=True)

  #remove response command
  @app_commands.command(
    name="response",
    description="lets you remove a word or phrase which the bot will respond to sad words with"
  )
  async def add_response(self, interaction: discord.Interaction, word: str):

    await interaction.response.defer()

    if is_admin(interaction) == True:
      guildId = interaction.guild.id #Gets the guild ID
  
      try: #Tests if that server already has a database section
        db[str(guildId)]
      except: #If not, it creates one
        db[str(guildId)] = {"sad_words": ["sad", "depressed", "upset", "unhappy", "not happy", "angry", "miserable", "feeling down"], "responses": ["cheer up!", "it's ok.", "don't listen to the bully, his words are wrong.", "you know what's good about hitting rock bottom, there's only one way left to go, and that's, up!"], "enabled":True}
        print("Created new database for: ", guildId)
  
      #removes the word
      guildDB = db[str(guildId)]
      rWords = guildDB['responses']
  
      if not any(words in word.lower() for words in rWords):
        await interaction.followup.send("Word could not be found.", ephemeral=True)
      else:
        rWords.remove(word.lower())
        await interaction.followup.send(f"successfully removed the word **{word}** to your server's list of responses!", ephemeral=True)

    else:
      await interaction.followup.send("You must be an admin to use this command!", ephemeral=True)
#End Remove class

cmds.add_command(Remove()) #Adds Remove class commands


#Begin List class
@app_commands.guild_only()
class List(app_commands.Group):

  #list sadwords command
  @app_commands.command(
    name="sad-words",
    description="shows all sad words the bot will respond with in this server"
  )
  async def list_sad_word(self, interaction: discord.Interaction):

    await interaction.response.defer()

    guildId = interaction.guild.id #Gets the guild ID

    try: #Tests if that server already has a database section
      db[str(guildId)]
    except: #If not, it creates one
      db[str(guildId)] = {"sad_words": ["sad", "depressed", "upset", "unhappy", "not happy", "angry", "miserable", "feeling down"], "responses": ["cheer up!", "it's ok.", "don't listen to the bully, his words are wrong.", "You know what's good about hitting rock bottom, there's only one way left to go, and that's, up!"], "enabled":True}
      print("Created new database for: ", guildId)

    #lists the words
    guildDB = db[str(guildId)]
    sWords = guildDB['sad_words']
    wrds = ""

    for i in sWords:
      wrds = wrds + i + ", "

    await interaction.followup.send(embed=discord.Embed(
      title="Sad Words",
      description=wrds,
      color=5763719
    ), ephemeral=True)


  #list responses command
  @app_commands.command(
    name="responses",
    description="lets you remove a word or phrase which the bot will respond to sad words with"
  )
  async def list_response(self, interaction: discord.Interaction):

    await interaction.response.defer()

    guildId = interaction.guild.id #Gets the guild ID

    try: #Tests if that server already has a database section
      db[str(guildId)]
    except: #If not, it creates one
      db[str(guildId)] = {"sad_words": ["sad", "depressed", "upset", "unhappy", "not happy", "angry", "miserable", "feeling down"], "responses": ["cheer up!", "it's ok.", "don't listen to the bully, his words are wrong.", "you know what's good about hitting rock bottom, there's only one way left to go, and that's, up!"], "enabled":True}
      print("Created new database for: ", guildId)

    #lists the words
    guildDB = db[str(guildId)]
    rWords = guildDB['responses']
    wrds = ""

    for i in rWords:
      wrds = wrds + i + ", "

    await interaction.followup.send(embed=discord.Embed(
      title="Responses",
      description=wrds,
      color=5763719
    ), ephemeral=True)

#End List class

cmds.add_command(List()) #Adds List class commands

#Begin Toggle class
@app_commands.guild_only()
class Toggle(app_commands.Group):

  #Toggle responses command
  @app_commands.command(
    name="responses",
    description="lets enable or disable responses on this server"
  )
  async def add_response(self, interaction: discord.Interaction, enabled: bool):

    await interaction.response.defer()

    if is_admin(interaction) == True:
      guildId = interaction.guild.id #Gets the guild ID
  
      try: #Tests if that server already has a database section
        db[str(guildId)]
      except: #If not, it creates one
        db[str(guildId)] = {"sad_words": ["sad", "depressed", "upset", "unhappy", "not happy", "angry", "miserable", "feeling down"], "responses": ["cheer up!", "it's ok.", "don't listen to the bully, his words are wrong.", "you know what's good about hitting rock bottom, there's only one way left to go, and that's, up!"], "enabled":True}
        print("Created new database for: ", guildId)
  
      #lists the words
      guildDB = db[str(guildId)]
      guildDB['enabled'] = enabled
  
      if enabled:
        await interaction.followup.send("**Enabled** responses to sad messages!", ephemeral=True)
  
      else:
        await interaction.followup.send("**Disabled** responses to sad messages.", ephemeral=True)

    else:
      await interaction.followup.send("You must be an admin to use this command!", ephemeral=True)

#End Toggle class

cmds.add_command(Toggle()) #Adds List class commands

#END database section


@cmds.command(
  name="inspire",
  description="sends an encouraging message in the channel"
)
async def inspire_command(interaction):
  await interaction.response.defer()
  await interaction.followup.send(get_quote())

@cmds.command(
  name="commands",
  description="sends an embed with information on all of the commands the bot has",
)
async def commands_command(interaction: discord.Interaction):
  await interaction.response.defer()
  await interaction.followup.send(embed=discord.Embed(
            title='commands',
            description=
            "**/help** \n displays some basic commands. \n **/inspire** \n sends an encouraging message to your server. \n**/commands** \nSends this embed. \n **/invite** \n use this command to invite the bot to your server or get invited to the bots server. \n **/update** \n sends you a message with information about the most recent update. \n **/bibleverse** \n use this command to get an inspiring bible verse sent to that channel. \n **/challenge** \n gives you information on the most recent challenge. \n **/add sad-word** \n use this command to add a sad word that the bot will respond to in this server. \n **/remove sad-word** \n use this command to remove a sad word that the bot will respond to in this server. \n **/list sad-words** \n use this command to list the sad words that the bot will respond to in this server. \n **/add response** \n use this command to add a response to sad words that the bot will use in this server. \n **/remove response** \n use this command to remove a response to sad words that the bot will use in this server. \n **/list responses** \n use this command to list the responses to sad words that the bot will use in this server. \n **/toggle responses** \n use this command to enable or disable responses to sad words in this server. (all sad words and responses will be saved).",
            color=5763719))

@cmds.command(
  name="invite",
  description="sends an embed with an invite link for this discord bot",
)
async def invite_command(interaction):
  await interaction.response.defer()
  await interaction.followup.send(embed=discord.Embed(
            title='Invites',
            description='Would you like to join our server or invite our bot to your own server?',            color=5763719).set_thumbnail(url='https://cdn.discordapp.com/avatars/791768754518228992/de612a16673514fb68f76769c1ac0da5.webp?size=640').add_field(name="Bot Invite", value="Click [here](https://discord.com/api/oauth2/authorize?client_id=791768754518228992&permissions=277025614912&scope=bot%20applications.commands) to invite the bot to your server!").add_field(name="Server Invite", value="Click [here](https://discord.gg/QSGMPbm36U) to join our server!").set_footer(text="NOTE: The first 100 users to join the Discord server will get the OG User role."))

@cmds.command(
  name="update",
  description="sends an embed with information on the most recent update",
)
async def update_command(interaction):
  await interaction.response.defer()
  await interaction.followup.send(embed=discord.Embed(
            title='Most recent Update:',
            description=
            """**Bug Fix** \nSome commands were not properly being executed due to responses taking too long. This update aims to fix that.""",
            color=5763719))

@cmds.command(
  name="challenge",
  description="sends an embed with information on the current challenge",
)
async def challenge_command(interaction):
  await interaction.response.defer()
  await interaction.followup.send(embed=discord.Embed(
            title='current challenge:',
            description=f'Customization has been implemented! Our new goal is to hit 100 servers! If that happens we will not only verify the bot but we will also add a way for you to encourage a friend specifically! \n `server count: {len(client.guilds)}`',
            color=5763719
        ))

@cmds.command(
  name="bibleverse",
  description="sends a message with an encouraging bible verse",
)
async def bible_command(interaction):
  await interaction.response.defer()
  await interaction.followup.send(get_verse())

#sad words command
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  mgld = message.guild

  if not mgld:
    guildId = "DMs"

  else:
    guildId = message.guild.id

  try:
    db[str(guildId)]

  except:
    db[str(guildId)] = {"sad_words": ["sad", "depressed", "upset", "unhappy", "not happy", "angry", "miserable", "feeling down"], "responses": ["cheer up!", "it's ok.", "don't listen to the bully, his words are wrong.", "you know what's good about hitting rock bottom, there's only one way left to go, and that's, up!"], "enabled":True}
    print("Created new database for: ", guildId)

  guildDB = db[str(guildId)]
  sWords = guildDB['sad_words']
  responses = guildDB['responses']
  status = guildDB['enabled']

  if message.content.startswith('^botservers'):
    await message.channel.send(f"I'm in {len(client.guilds)} servers!")

  if any(word in msg.lower() for word in sWords) and status:
    await message.channel.send(random.choice(responses))

keep_alive()

client.run(os.getenv('TOKEN'))