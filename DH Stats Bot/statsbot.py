import os
import json
import urllib.request
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# Function for adding users into the users directory and handling stats.
@client.event
async def on_message(message):
    user_id = str(message.author.id)

    user_dict = {}

    with open("users.txt") as usersfile:
        for line in usersfile:
            (u_id, u_roid) = line.split()
            user_dict[u_id] = u_roid

    if message.author == client.user:
        return
    
    # Creating a new user file with their discord ID and provided ROID.
    elif "!addme" in message.content.lower():

        if len(message.content) < 24:
            await message.channel.send("Please provide your ROID" \
                                        " along with the command.")

        elif len(message.content) == 24:
            roid = str(message.content[7:24])

            if user_id in user_dict:
                await message.channel.send("You already exist in my database!" \
                                            " No need to do it again!")

            elif user_id not in user_dict:
                userfile = open("users.txt", "a")
                userfile.write(user_id)
                userfile.write(" ")
                userfile.write(roid)
                userfile.write("\n")
                userfile.close()

                await message.channel.send("You have been added.")

        elif len(message.content) > 24:
            await message.channel.send("Please provide a valid ROID.")

    # Gets a player's stats from the website and displays them to the user.
    elif "!stats" in message.content.lower():

        if user_id in user_dict:
            user_roid = user_dict[user_id]

            stats_url = "http://api.darklightgames.com/players/" \
                         + user_roid + "/?format=json"

            user_data = urllib.request.urlopen(stats_url)
            stats_contents = user_data.read()
            load_stats = json.loads(stats_contents)

            kills = "**Kills:** " + str(load_stats["kills"]) + " "
            deaths = "| **Deaths:** " + str(load_stats["deaths"]) + " "
            raw_kdr = str(load_stats["kills"] / load_stats["deaths"])
            kdr = "| **Kill-Death Ratio:** " + str(raw_kdr[0:4]) + " "
            ff_kills = "| **FF Kills:** " + str(load_stats["ff_kills"]) + " "
            ff_deaths = "| **FF Deaths:** " + str(load_stats["ff_deaths"]) + " "
            stats = kills + deaths + kdr + ff_kills + ff_deaths

            await message.channel.send(stats)

        elif user_id not in user_dict:
            await message.channel.send("I couldn't find you in my storage!\n" \
                                        "Please make sure you added yourself first!")
            await message.channel.send("Use `!commands`" \
                                        " to see a list of commands.")


    elif "!commands" in message.content.lower():
        await message.channel.send("https://i.imgur.com/79GCqL1.png")
    

client.run(TOKEN)