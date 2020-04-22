import os
import discord
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()


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
        if user_id in user_dict:
            user_roid = user_dict[user_id]

            stats_url = "http://api.darklightgames.com/players/" + user_roid + "/?format=json"

            # Opens a user's page on the stats website and grabs their stats (kills, deaths, etc)
            stats_data = urllib.request.urlopen(stats_url)
            stats_contents = stats_data.read()
            load_stats = json.loads(stats_contents)

            weapon_url =  "http://46.101.44.19/players/damage_type_kills/?format=json&killer_id=" + user_roid + \
                          "&limit=10&offset=0"
            
            # Opens a user's weapon data file and loads it's contents
            weapon_data = urllib.request.urlopen(weapon_url)
            weapon_contents = weapon_data.read()
            weapon_list = str(weapon_contents).split("{")

            # Getting a user's favorite weapon and kill count with said weapon
            top_weapon = weapon_list[2]
            split_list = top_weapon.split(",")
            trimmed_list = [element.strip("}") for element in split_list]
            del trimmed_list[-1]

            stat_dict = {}

            for element in trimmed_list:
                (key, val) = element.split(":")
                stat_dict[key] = val

            # Dict to reference a given damage type and give it a proper name
            dh_weapon_dict = {
                '"DH_MG34DamType"'                  : "MG34",
                '"DH_MP40DamType"'                  : "MP40",
                '"DH_PPSH41DamType"'                : "PPSH-41 Drum",
                '"DH_DP28DamType"'                  : "DP28",
                '"DH_30calDamType"'                 : "30 Cal. MG",
                '"DH_BARDamType"'                   : "BAR",
                '"DH_ThompsonDamType"'              : "Thompson",
                '"DH_MG42DamType"'                  : "MG42",
                '"DH_Kar98DamType"'                 : "Kar98",
                '"DH_M1GarandDamType"'              : "M1 Garand",
                '"DH_StenMkIIDamType"'              : "Sten Mk. II",
                '"DH_STG44DamType"'                 : "STG 44",
                '"DH_G43DamType"'                   : "Gewehr 43",
                '"DH_M1CarbineDamType"'             : "M1 Carbine",
                '"DH_GreaseGunDamType"'             : "M3 Grease Gun",
                '"DH_SVT40DamType"'                 : "SVT-40",
                '"DH_EnfieldNo4DamType"'            : "Enfield No.4",
                '"DH_PPD40DamType"'                 : "PPD-40",
                '"DH_M38DamType"'                   : "M38",
                '"DH_BesaDamType"'                  : "Besa",
                '"DH_TT33DamType"'                  : "TT-33",
                '"DH_MN9130DamType"'                : "MN-9130",
                '"DH_BrenDamType"'                  : "Bren",
                '"DH_Winchester1897DamType"'        : "Winchester 1897",
                '"DH_PTRDDamType"'                  : "PTRD-41",
                '"DH_SpringfieldScopedDamType"'     : "Springfield",
                '"DH_PPS43DamType"'                 : "PPS-43",
                '"DH_FG42DamType"'                  : "FG42",
                '"DH_Kar98ScopedDamType"'           : "Scoped Kar98",
                '"DH_50CalDamType"'                 : "50 Cal. MG",
                '"DH_P38DamType"'                   : "Walther P38",
                '"DH_G41DamType"'                   : "Gewehr 41",
                '"DH_G43ScopedDamType"'             : "Scoped Gewehr 43",
                '"DH_MP41DamType"'                  : "MP41",
                '"DH_ColtM1911DamType"'             : "Colt M1911",
                '"DH_C96DamType"'                   : "Mauser C96",
                '"DH_PPSH41_stickDamType"'          : "PPSH-41 35rnd",
                '"DH_EnfieldNo2DamType"'            : "Enfield No.2",
                '"DH_AVT40DamType"'                 : "AVT-40",
                '"DH_Nagant1895DamType"'            : "Nagant 1895",
                '"DH_M44DamType"'                   : "MN-M44 Carbine",
                '"DH_MN9130ScopedDamType"'          : "Scoped MN-9130",
                '"DH_BazookaImpactDamType"'         : "Bazooka",
                '"DH_PanzerschreckImpactDamType"'   : "Panzerschreck",
                '"DH_PanzerFaustImpactDamType"'     : "Panzerfaust",
                '"DH_StielGranateDamType"'          : "Stielhandgranate",
                '"DH_F1GrenadeDamType"'             : "F1 Grenade",
                '"DH_M1GrenadeDamType"'             : "M1 Grenade",
                '"DHShellHE75mmDamageType"'         : "75mm HE",
                '"DHShellHE75mmATDamageType"'       : "75mm HEAT",
                '"DHArtillery105DamageType"'        : "Artillery 105mm",
                '"DHShellHE105mmDamageType"'        : "105mm HE",
                '"DHShellHE37mmDamageType"'         : "37mm HE",
                '"DHShellHE50mmATDamageType"'       : "50mm HEAT",
                '"DHShellAPGunImpactDamageType"'    : "AP Shell"
            }

            # Reads a user's top damage type and associates it with a weapon name
            dam_type = stat_dict['"damage_type_id"']
            ref_weapon = dh_weapon_dict[dam_type]

            fav_weapon = "**Favorite Weapon:** " + ref_weapon + " at " + \
                        stat_dict['"kills"'] + " kills"
            
            # Constructing the user's stats for display in Discord
            s_kills = "**Kills:** " + str(load_stats["kills"]) + " "

            deaths = "| **Deaths:** " + str(load_stats["deaths"]) + " "

            raw_kdr = str(load_stats["kills"] / load_stats["deaths"])

            kdr = "| **Kill-Death Ratio:** " + str(raw_kdr[0:4]) + " "

            stats = " " + s_kills + deaths + kdr + "| " + fav_weapon

            # Mention the user who called "!stats" and display their stats in Discord
            await message.channel.send(message.author.mention + stats)
    
        elif user_id not in user_dict:
            await message.channel.send("You do not exist in my storage, make sure you added yourself first.")
            await message.channel.send("Use `!commands` to see a list of commands.")
        
    elif "!commands" in message.content.lower():
        await message.channel.send("https://i.imgur.com/79GCqL1.png")


client.run(TOKEN)