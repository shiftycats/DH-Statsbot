import os
import discord
from dotenv import load_dotenv
from discord.ext import tasks

import servers
import stats

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()

# Variables used to keep track of selecting a map with the !map stats command.
in_progress = 0
map_name = None
maps_temp = None

# Task-loop to update the bot's status-message with the current playercount.
@tasks.loop(minutes=2)
async def statusUpdate():
    playercount = servers.statusUpdate()

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=playercount))


# Display message to the terminal when bot is connected to Discord
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    # If the message author is statsbot, don't do anything
    if message.author == client.user:
        return
    
    # Creating a dictionary from users.txt
    # Keys are user's Discord ID, values are their provided ROID
    user_dict = {}

    with open("users.txt") as usersfile:
        for line in usersfile:
            (u_id, u_roid) = line.split()
            user_dict[u_id] = u_roid

    # User-ID string used for referencing their ROID easily.
    user_id = str(message.author.id)


    # Adding a user's ID and provided ROID to users.txt
    if "!addme" in message.content.lower():
        if len(message.content) > 24:
            await message.channel.send("Please provide a valid ROID with the command.")
        
        elif len(message.content) < 24:
            await message.channel.send("Please provide a valid ROID with the command.")
        
        elif len(message.content) == 24:
            roid = str(message.content[7:24])

            # Check if they already exist in users.txt
            if user_id in user_dict:
                await message.channel.send("You already exist in my database.")
            
            elif user_id not in user_dict:
                userfile = open("users.txt", "a")
                userfile.write(user_id)
                userfile.write(" ")
                userfile.write(roid)
                userfile.write("\n")
                userfile.close()

                print("Added a new user")
                await message.channel.send("You have been added.")


    elif "!stats" in message.content.lower():
        msg = stats.userStats(user_dict, user_id)

        await message.channel.send(message.author.mention + msg)


    elif "!ffstats" in message.content.lower():
        msg = stats.ffStats(user_dict, user_id)

        await message.channel.send(message.author.mention + msg)
    

    elif message.content.startswith("!map stats"):
        global in_progress

        # Check if a user is already using the command to prevent being interupted.
        if in_progress == 0:
            global map_name
            global maps_temp

            msg, selected_map, map_list, response_flag = stats.mapSearch(message.content)

            map_name = selected_map
            maps_temp = map_list

            # Check what response mapSearch() returns, respond accordingly.
            # 0 = map was found, give a choice | 1 = map was not found.
            if response_flag == 0:
                in_progress += 1

                selection_msg = " Which game-mode? " + "`" + msg + "`"
                await message.channel.send(message.author.mention + selection_msg)
            elif response_flag == 1:
                await message.channel.send(message.author.mention + msg)
        elif in_progress == 1:
            await message.channel.send(message.author.mention + " The command is waiting for a reply first, please make a selection (1-4).")


    elif "1" in message.content and in_progress == 1:
        mode_selection = maps_temp[int(message.content) - 1]

        prefix = map_name
        msg = stats.mapStats(mode_selection)

        in_progress -= 1
        map_name = None
        maps_temp = None

        await message.channel.send(prefix + "\n" + msg)
    

    elif "2" in message.content and in_progress == 1:
        mode_selection = maps_temp[int(message.content) - 1]

        prefix = map_name
        msg = stats.mapStats(mode_selection)

        in_progress -= 1
        map_name = None
        maps_temp = None

        await message.channel.send(prefix + "\n" + msg)


    elif "3" in message.content and in_progress == 1:
        mode_selection = maps_temp[int(message.content) - 1]

        prefix = map_name
        msg = stats.mapStats(mode_selection)

        in_progress -= 1
        map_name = None
        maps_temp = None

        await message.channel.send(prefix + "\n" + msg)


    elif "4" in message.content and in_progress == 1:
        mode_selection = maps_temp[int(message.content) - 1]

        prefix = map_name
        msg = stats.mapStats(mode_selection)

        in_progress -= 1
        map_name = None
        maps_temp = None

        await message.channel.send(prefix + "\n" + msg)


    elif "!servers" in message.content.lower():
        output = servers.serverList()

        await message.channel.send("```" + output + "```")


    elif "!commands" in message.content.lower():
        addme_cmd = "!addme (ROID)         - Adds you to the bot's database, 1-time command."
        stats_cmd = "!stats                - Displays your general stats."
        ffstats_cmd = "!ffstats              - Displays your friendly-fire stats."
        mapstats_cmd = "!map stats (map_name) - Displays stats for a given map."
        #wareffort_cmd = "!wareffort            - Displays the progress of the war."
        servers_cmd = "!servers              - Displays real-time server-pop and the map being played."
        info_cmd = "!info                 - DM's some short info about Statsbot"

        cmds_message = "```" + addme_cmd + "\n" + stats_cmd + "\n" + ffstats_cmd + "\n" + mapstats_cmd + "\n" + servers_cmd + "\n" + info_cmd + "```"

        await message.channel.send(cmds_message)


    elif "!info" in message.content.lower():
        contact_info = "DH-Statsbot is developed and maintained by Chaussettes#8027. All questions can be happily routed to them, they are always happy to help out."
        github_info = "The code for Statsbot is hosted on github, here you can find more info about it and read some general disclaimers:"
        github_link = "https://github.com/Chaussettes99/DH-Statsbot"

        await message.author.send(contact_info + "\n" + github_info + "\n" + github_link)


    statusUpdate.start()

client.run(TOKEN)
