import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()

sad_words = ["sad","depressed","unhappy","angry","frustrated","i cant do it","i dont know what to do","feel miserable","feeling terrible"]

starter_encouragements = ["Cheer up!", "Hang in there!", "You're doing great,friend!","You are capable of anything!","You're a strong person!"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db("encouragements")
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event #register event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))  #0 replaced with client -> client.user will run

@client.event
async def on_message(message):
  if message.author == client.user:
    return  

  msg = message.content

  if message.content.startswith('$hello'):
    await message.channel.send('Hello! How you doin?')

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  if "encouragements" in db.keys():
    # options = options + db["encouragements"].value
    options = options + db["encouragements"]

  if any(word in msg for word in sad_words):  #msg stands for message.content
    # await message.channel.send(random.choice(starter_encouragements))
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)


#client.run(os.getenv('TOKEN'))
client.run(os.environ['TOKEN'])

