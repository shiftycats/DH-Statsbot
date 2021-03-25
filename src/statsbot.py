import os
import discord
from dotenv import load_dotenv
from discord.ext import tasks
from datetime import datetime

import servers
import stats

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVERS_CHANNEL_ID = int(os.getenv("SERVERS_CHANNEL_ID"))
client = discord.Client()

# Variables used to keep track of selecting a map with the !map stats command.
in_progress = 0
map_name = None
maps_temp = None


# Task-loop to update info about game servers.
@tasks.loop(minutes=2)
async def statusUpdate():
    # Update player count status.
    playercount = servers.statusUpdate()

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=playercount))

    # Update server info channel.
    servers_channel = client.get_channel(SERVERS_CHANNEL_ID)

    try:
        my_last_message = await servers_channel.history().find(lambda m: m.author.id == client.user.id)
    except AttributeError:
        print("Failed to access servers channel", SERVERS_CHANNEL_ID);
        return

    timestamp = datetime.utcnow().strftime("Last updated: %b %d, %I:%M:%S %p UTC")
    servers_content = "`" + timestamp + "`\n```" + servers.serverList() + "```\n"

    if not my_last_message:
        await servers_channel.send(servers_content)
    else:
        await my_last_message.edit(content=servers_content)


# Display message to the terminal when bot is connected to Discord
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    statusUpdate.start()


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
        if len(message.content) != 24:
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


    # Builds and sends a large embedded reply with all user stats.
    elif "!stats" in message.content.lower():
        if user_id in user_dict:
            components = stats.userStats(user_dict, user_id)

            kills = components[0]
            deaths = components[1]
            kdr = components[2]
            weapon = components[3]
            tk_kills = components[4]
            tk_deaths = components[5]
            tk_ratio = components[6]

            user_nick = message.author.display_name
            pfp = message.author.avatar_url

            stats_embed = discord.Embed(
                title = "Stats for " + user_nick,
                color = discord.Colour.blue()
            )

            stats_embed.add_field(name="Kills", value=kills, inline=True)
            stats_embed.add_field(name="Deaths", value=deaths, inline=True)
            stats_embed.add_field(name="KDR", value=kdr, inline=True)
            stats_embed.add_field(name=weapon, value="\u200b", inline=False)
            stats_embed.add_field(name="FF Kills", value=tk_kills, inline=True)
            stats_embed.add_field(name="FF Deaths", value=tk_deaths, inline=True)
            stats_embed.add_field(name="TK Ratio", value=tk_ratio, inline=True)

            stats_embed.set_footer(text="stats.darklightgames.com")
            stats_embed.set_thumbnail(url=pfp)

            await message.channel.send(embed=stats_embed)
        
        elif user_id not in user_dict:
            msg = " You do not exist in my storage! Please make sure you added yourself first!"
            cmd_msg = "Use `!commands` to see a list of commands."

            await message.channel.send(message.author.mention + msg + "\n" + cmd_msg)


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


    # Check if the bot is waiting for a reply and the if user gives an appropiate answer.
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


    elif "!commands" in message.content.lower():
        addme_cmd = "!addme (ROID)         - Adds you to the bot's database, 1-time command."
        stats_cmd = "!stats                - Displays your stats."
        mapstats_cmd = "!map stats (map name) - Displays stats for a given map."
        info_cmd = "!info                 - DM's some short info about Statsbot"

        cmds_message = "```" + addme_cmd + "\n" + stats_cmd + "\n" + mapstats_cmd + "\n" + info_cmd + "```"

        await message.channel.send(cmds_message)


    elif "!info" in message.content.lower():
        contact_info = "DH-Statsbot is developed and maintained by Chaussettes#8027. All questions can be happily routed to them, they are always happy to help out."
        github_info = "The code for Statsbot is hosted on github, here you can find more info about it and read some general disclaimers:"
        github_link = "https://github.com/Chaussettes99/DH-Statsbot"

        await message.author.send(contact_info + "\n" + github_info + "\n" + github_link)

client.run(TOKEN)
