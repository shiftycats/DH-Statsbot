import os
import json
import discord
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import urllib.request
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
    
    # ---------------------------------------------------------------------------
    # GENERAL STATISTICS
    # This section handles displaying general stats to the user
    # Organized by kills + deaths + kd ratio + their favorite weapon (most kills)
    # ---------------------------------------------------------------------------
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
                '"DHShellAPGunImpactDamageType"'    : "AP Shell",
                '"DHShellImpactDamageType"'         : "Shell Impact"
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
    
    # -------------------------------------------------------------------------
    # TEAMKILL STATISTICS
    # This section handles displaying a user's friendly-fire statistics
    # Organized by ff-kills + ff-deaths + their ratio of tk's to normal kills +
    # their ratio of teamkill-deaths to normal deaths
    # -------------------------------------------------------------------------
    elif "!ffstats" in message.content.lower():
        if user_id in user_dict:
            user_roid = user_dict[user_id]

            stats_url = "http://api.darklightgames.com/players/" + user_roid + "/?format=json"

            stats_data = urllib.request.urlopen(stats_url)
            stats_contents = stats_data.read()
            load_stats = json.loads(stats_contents)

            ff_kills = "**FF Kills:** " + str(load_stats["ff_kills"]) + " "
            
            ff_deaths = "| **FF Deaths:** " + str(load_stats["ff_deaths"]) + " "

            raw_tk_ratio = int(load_stats["ff_kills"]) / int(load_stats["kills"])

            raw_death_ratio = int(load_stats["ff_deaths"]) / int(load_stats["deaths"])

            # Calculate teamkill and teamkill-death average.
            tk_rate = int(load_stats["kills"]) / int(load_stats["ff_kills"])
            death_rate = int(load_stats["deaths"]) / int(load_stats["ff_deaths"])

            # Move decimal-points over 2 places.
            tk_ratio = raw_tk_ratio * 10 * 10
            death_ratio = raw_death_ratio * 10 * 10

            formatted_tk_rate = "*(1 TK every {:.0f}*".format(tk_rate) + " *kills)*  "
            formatted_death_rate = "*(TK'd once every {:.0f}*".format(death_rate) + " *deaths)*"

            formatted_tk_ratio = "| **TK Ratio:** {:.2f}".format(tk_ratio) + "% " + formatted_tk_rate

            formatted_death_ratio = "| **Death Ratio:** {:.2f}".format(death_ratio) + "% " + formatted_death_rate

            stats = " " + ff_kills + ff_deaths + formatted_tk_ratio + formatted_death_ratio

            await message.channel.send(message.author.mention + stats)
    

    # ---------------------------------------------------------------------------------------------------
    # MAP STATISTICS
    # This section handles displaying specific map-statistics to the user
    # Map-faction-wins are read and a small infographic is drawn, showing weighted wins for each faction.
    # ---------------------------------------------------------------------------------------------------
    elif "!map stats" in message.content.lower():
        split_string = message.content.split()
        selected_map = split_string[2]

        map_dict = {
            "barashka"                : "DH-Barashka_Clash",
            "bois_jacques"            : "DH-Bois_Jacques_Push",
            "brecourt"                : "DH-Brecourt_Push",
            "bridgehead"              : "DH-Bridgehead_Advance",
            "caen"                    : "DH-Caen_Advance",
            "cambes_en_plaine"        : "DH-Cambes_En_Plaine_Clash",
            "carentan_causeway"       : "DH-Carentan_Causeway_Push",
            "carentan"                : "DH-Carentan_Push",
            "carpiquet_airfield"      : "DH-Carpiquet_Airfield_Advance",
            "cheneux_push"            : "DH-Cheneux_Push",
            "danzig"                  : "DH-Danzig_Push",
            "dead_mans_corner"        : "DH-Dead_Man's_Corner_Push",
            "dog_green"               : "DH-Dog_Green_Push",
            "donner"                  : "DH-Donner_Stalemate",
            "falaise"                 : "DH-Falaise_Push",
            "flakturm_tiergarten"     : "DH-Flakturm_Tiergarten_Push",
            "foucarville"             : "DH-Foucarville_Push",
            "foy"                     : "DH-Foy_Push",
            "ginkel_heath"            : "DH-Ginkel_Heath_Push",
            "gorlitz"                 : "DH-Gorlitz_Push",
            "grey_ghosts_of_war"      : "DH-Grey_Ghosts_Of_War_Stalemate",
            "gunassault"              : "DH-GunAssault",
            "hattert"                 : "DH-Hattert_Clash",
            "hedgerow_hell"           : "DH-Hedgerow_Hell_Clash",
            "hill_108"                : "DH-Hill_108_Push",
            "hill_400"                : "DH-Hill_400_Push",
            "hurtgenwald"             : "DH-Hurtgenwald_Push",
            "juno_beach"              : "DH-Juno_Beach_Push",
            "konigsplatz"             : "DH-Konigsplatz_Push",
            "kriegstadt_advance"      : "DH-Kriegstadt_Advance",
            "kriegstadt_push"         : "DH-Kriegstadt_Push",
            "la_cambe_advance"        : "DH-La_Cambe_Advance",
            "la_cambe_push"           : "DH-La_Cambe_Push",
            "la_chapelle"             : "DH-La_Chapelle_Push",
            "la_gleize_advance"       : "DH-La_Gleize_Advance",
            "la_gleize_push"          : "DH-La_Gleize_Push",
            "lutremange_advance"      : "DH-Lutremange_Advance",
            "lutremange_push"         : "DH-Lutremange_Push",
            "noville_advance"         : "DH-Noville_Advance",
            "noville_push"            : "DH-Noville_Push",
            "nuenen_advance"          : "DH-Nuenen_Advance",
            "nuenen_push"             : "DH-Nuenen_Push",
            "nuenen_clash"            : "DH-Nuenen_Clash",
            "olgedow"                 : "DH-Olgedow_Clash",
            "oosterbeek"              : "DH-Oosterbeek_Advance",
            "pariserplatz"            : "DH-Pariserplatz_Push",
            "poteau_ambush_push"      : "DH-Poteau_Ambush_Push",
            "putot_en_bessin_advance" : "DH-Putot_En_Bessin_Advance",
            "rabenheck"               : "DH-Rabenheck_Advance",
            "radar"                   : "DH-Radar_Advance",
            "raids"                   : "DH-Raids_Push",
            "rakowice"                : "DH-Rakowice_Push",
            "reichswald_advance"      : "DH-Reichswald_Advance",
            "reichswald_push"         : "DH-Reichswald_Push",
            "salaca_river"            : "DH-Salaca_River_Clash",
            "san_valentino"           : "DH-San_Valentino_Advance",
            "simonskall"              : "DH-Simonskall_Push",
            "st-clement"              : "DH-St-Clement_Push",
            "stavelot"                : "DH-Stavelot_Push",
            "stoumont_advance"        : "DH-Stoumont_Advance",
            "stoumont_push"           : "DH-Stoumont_Push",
            "targnon"                 : "DH-Targnon_Push",
            "ten_aard"                : "DH-Ten_Aard_Push",
            "valko"                   : "DH-Valko_Advance",
            "varaville"               : "DH-Varaville_Advance",
            "vierville"               : "DH-Vierville_Push",
            "vossenack"               : "DH-Vossenack_Push",
            "arad"                    : "DH-WIP_Arad_Advance",
            "arnhem_bridge"           : "DH-WIP_Arnhem_Bridge_Push",
            "berezina"                : "DH-WIP_Berezina_Advance",
            "black_day_july"          : "DH-WIP_Black_Day_July_Advance",
            "butovo"                  : "DH-WIP_Butovo_Advance",
            "chambois"                : "DH-WIP_Chambois_Push",
            "champs"                  : "DH-WIP_Champs_Push",
            "cheneux_advance"         : "DH-WIP_Cheneux_Advance",
            "cholm"                   : "DH-WIP_Cholm_Advance",
            "dom_pavlova"             : "DH-WIP_Dom_Pavlova_Advance",
            "fallen_heroes"           : "DH-WIP_FallenHeroes_Clash",
            "fury"                    : "DH-WIP_Fury_Clash",
            "godolli"                 : "DH-WIP_Godolli_Push",
            "kasserine_pass"          : "DH-WIP_Kasserine_Pass_Advance",
            "klin_1941"               : "DH-WIP_Klin1941_Advance",
            "kommerscheidt"           : "DH-WIP_Kommerscheidt_Advance",
            "krasnyi_oktyabr"         : "DH-WIP_Krasnyi_Oktyabr_Defence",
            "kryukovo"                : "DH-WIP_Kryukovo_Push",
            "la_fiere"                : "DH-WIP_La_Fiere_Advance",
            "la_fiere_day"            : "DH-WIP_La_Fiere_Day_Advance",
            "leningrad"               : "DH-WIP_Leningrad_Push",
            "leszinow"                : "DH-WIP_Lesinow_Advance",
            "lyes_krovy"              : "DH-WIP_Lyes_Krovy_Defence",
            "makhnovo"                : "DH-WIP_Makhnovo_Advance",
            "maupertus"               : "DH-WIP_Maupertus_Push",
            "merderet"                : "DH-WIP_Merderet_Advance",
            "myshkova_river"          : "DH-WIP_Myshkova_River_Advance",
            "nyiregyhaza"             : "DH-WIP_Nyiregyhaza_Push",
            "odessa"                  : "DH-WIP_Odessa_Push",
            "olkhovatka"              : "DH-WIP_Olkhovatka_Advance",
            "omaha_beach"             : "DH-WIP_OmahaBeach_Push",
            "pegasus_bridge"          : "DH-WIP_Pegasus_Bridge_Advance",
            "pointe_du_hoc"           : "DH-WIP_Pointe_Du_Hoc_Push",
            "port-en-bessin"          : "DH-WIP_Port-En-Bessin_Push",
            "poteau_ambush_advance"   : "DH-WIP_Poteau_Ambush_Advance",
            "prussia"                 : "DH-WIP_Prussia_Push",
            "ramelle"                 : "DH-WIP_Ramelle_Push",
            "red_god_of_war"          : "DH-WIP_Red_God_Of_War_Push",
            "remagen"                 : "DH-WIP_Remagen_Clash",
            "rhine_river"             : "DH-WIP_Rhine_River_Clash",
            "riga_docks"              : "DH-WIP_Riga_Docks_Push",
            "schijndel"               : "DH-WIP_Schijndel_Advance",
            "smolensk_advance"        : "DH-WIP_Smolensk_Advance",
            "smolensk_stalemate"      : "DH-WIP_Smolensk_Stalemate",
            "st_marie_du_mont"        : "DH-WIP_St_Marie_Du_Mont_Advance",
            "stalingrad_kessel"       : "DH-WIP_Stalingrad_Kessel_Push",
            "tula_outskirts"          : "DH-WIP_TulaOutskirts_Push",
            "turqueville"             : "DH-WIP_Turqueville_Push",
            "wanne"                   : "DH-WIP_Wanne_Advance",
            "winter_stalemate"        : "DH-WIP_Winter_Stalemate_Clash",
            "zhitomir_1941"           : "DH-WIP_Zhitomir1941_Push"
        }

        if selected_map in map_dict:
            map_string = map_dict[selected_map]

            # Open the selected map's data and parse it.
            map_url = "http://46.101.44.19/maps/" + map_string + "/summary/"
            map_data = urllib.request.urlopen(map_url)
            map_data_contents = map_data.read()
            load_map_data = json.loads(map_data_contents)

            # Define json objects for easier use.
            axis_w = int(load_map_data["axis_wins"])
            axis_d = int(load_map_data["axis_deaths"])
            allied_w = int(load_map_data["allied_wins"])
            allied_d = int(load_map_data["allied_deaths"])

            axis_deaths = "**Axis Deaths:** " + str(axis_d) + " "
            allied_deaths = "| **Allied Deaths:** " + str(allied_d)
            axis_wins = "| **Axis Wins:** " + str(axis_w) + "  "
            allied_wins = "  **Allied Wins:** " + str(allied_w) + " "

            number_line = ["«", "-", "-", "-", "-",
                        "-", "-", "-", "-", "-",
                        "-", "-", "-", "-", "-",
                        "-", "-", "-", "-", "-",
                        "»"]

            total_games = axis_w + allied_w

            # Compare the map's axis vs allied wins.
            # Draw a small line-infographic weighted towards the larger winrate.
            if axis_w > allied_w:
                rough_percentage = axis_w / total_games
                win_percentage = round(rough_percentage, 2)

                marker_shift = 20 * win_percentage

                marker_position = 20 - marker_shift

                number_line.insert(int(marker_position), "o")
                win_infographic = ''.join(number_line)
            elif axis_w < allied_w:
                rough_percentage = allied_w / total_games
                win_percentage = round(rough_percentage, 2)

                marker_shift = 20 * win_percentage

                number_line.insert(int(marker_shift), "o")
                win_infographic = ''.join(number_line)

            composed_map_message = axis_deaths + axis_wins + win_infographic + allied_wins + allied_deaths

            await message.channel.send(composed_map_message)
        
        elif selected_map not in map_dict:
            await message.channel.send("I do not have that map included, sorry.")
    

    # ---------------------------------------------------------------------------------------
    # WAR-EFFORT STATISTICS
    # Tracks the total status of the "war."
    # EX: Total kills for all maps and which faction is winning based on individual map wins.
    # ---------------------------------------------------------------------------------------
    elif "!wareffort" in message.content.lower():
        await message.channel.send("Calculating the total progress of the war, please wait up to 1 minute.", delete_after=1)

        map_list = [
            "DH-Barashka_Clash",
            "DH-Bois_Jacques_Push",
            "DH-Brecourt_Push",
            "DH-Bridgehead_Advance",
            "DH-Caen_Advance",
            "DH-Cambes_En_Plaine_Clash",
            "DH-Carentan_Causeway_Push",
            "DH-Carentan_Push",
            "DH-Carpiquet_Airfield_Advance",
            "DH-Cheneux_Push",
            "DH-Danzig_Push",
            "DH-Dead_Man's_Corner_Push",
            "DH-Dog_Green_Push",
            "DH-Donner_Stalemate",
            "DH-Falaise_Push",
            "DH-Flakturm_Tiergarten_Push",
            "DH-Foucarville_Push",
            "DH-Foy_Push",
            "DH-Ginkel_Heath_Push",
            "DH-Gorlitz_Push",
            "DH-Grey_Ghosts_Of_War_Stalemate",
            "DH-GunAssault",
            "DH-Hattert_Clash",
            "DH-Hedgerow_Hell_Clash",
            "DH-Hill_108_Push",
            "DH-Hill_400_Push",
            "DH-Hurtgenwald_Push",
            "DH-Juno_Beach_Push",
            "DH-Konigsplatz_Push",
            "DH-Kriegstadt_Advance",
            "DH-Kriegstadt_Push",
            "DH-La_Cambe_Advance",
            "DH-La_Cambe_Push",
            "DH-La_Chapelle_Push",
            "DH-La_Gleize_Advance",
            "DH-La_Gleize_Push",
            "DH-Lutremange_Advance",
            "DH-Lutremange_Push",
            "DH-Noville_Advance",
            "DH-Noville_Push",
            "DH-Nuenen_Advance",
            "DH-Nuenen_Push",
            "DH-Nuenen_Clash",
            "DH-Olgedow_Clash",
            "DH-Oosterbeek_Advance",
            "DH-Pariserplatz_Push",
            "DH-Poteau_Ambush_Push",
            "DH-Putot_En_Bessin_Advance",
            "DH-Rabenheck_Advance",
            "DH-Radar_Advance",
            "DH-Raids_Push",
            "DH-Rakowice_Push",
            "DH-Reichswald_Advance",
            "DH-Reichswald_Push",
            "DH-Salaca_River_Clash",
            "DH-San_Valentino_Advance",
            "DH-Simonskall_Push",
            "DH-St-Clement_Push",
            "DH-Stavelot_Push",
            "DH-Stoumont_Advance",
            "DH-Stoumont_Push",
            "DH-Targnon_Push",
            "DH-Ten_Aard_Push",
            "DH-Valko_Advance",
            "DH-Varaville_Advance",
            "DH-Vierville_Push",
            "DH-Vossenack_Push",
            "DH-WIP_Arad_Advance",
            "DH-WIP_Arnhem_Bridge_Push",
            "DH-WIP_Berezina_Advance",
            "DH-WIP_Black_Day_July_Advance",
            "DH-WIP_Butovo_Advance",
            "DH-WIP_Chambois_Push",
            "DH-WIP_Champs_Push",
            "DH-WIP_Cheneux_Advance",
            "DH-WIP_Cholm_Advance",
            "DH-WIP_Dom_Pavlova_Advance",
            "DH-WIP_FallenHeroes_Clash",
            "DH-WIP_Fury_Clash",
            "DH-WIP_Godolli_Push",
            "DH-WIP_Kasserine_Pass_Advance",
            "DH-WIP_Klin1941_Advance",
            "DH-WIP_Kommerscheidt_Advance",
            "DH-WIP_Krasnyi_Oktyabr_Defence",
            "DH-WIP_Kryukovo_Push",
            "DH-WIP_La_Fiere_Advance",
            "DH-WIP_La_Fiere_Day_Advance",
            "DH-WIP_Leningrad_Push",
            "DH-WIP_Lesinow_Advance",
            "DH-WIP_Lyes_Krovy_Defence",
            "DH-WIP_Makhnovo_Advance",
            "DH-WIP_Maupertus_Push",
            "DH-WIP_Merderet_Advance",
            "DH-WIP_Myshkova_River_Advance",
            "DH-WIP_Nyiregyhaza_Push",
            "DH-WIP_Odessa_Push",
            "DH-WIP_Olkhovatka_Advance",
            "DH-WIP_OmahaBeach_Push",
            "DH-WIP_Pegasus_Bridge_Advance",
            "DH-WIP_Pointe_Du_Hoc_Push",
            "DH-WIP_Port-En-Bessin_Push",
            "DH-WIP_Poteau_Ambush_Advance",
            "DH-WIP_Prussia_Push",
            "DH-WIP_Ramelle_Push",
            "DH-WIP_Red_God_Of_War_Push",
            "DH-WIP_Remagen_Clash",
            "DH-WIP_Rhine_River_Clash",
            "DH-WIP_Riga_Docks_Push",
            "DH-WIP_Schijndel_Advance",
            "DH-WIP_Smolensk_Advance",
            "DH-WIP_Smolensk_Stalemate",
            "DH-WIP_St_Marie_Du_Mont_Advance",
            "DH-WIP_Stalingrad_Kessel_Push",
            "DH-WIP_TulaOutskirts_Push",
            "DH-WIP_Turqueville_Push",
            "DH-WIP_Wanne_Advance",
            "DH-WIP_Winter_Stalemate_Clash",
            "DH-WIP_Zhitomir1941_Push"
        ]

        # Dictionaries for storing all values from all maps for arithmetic-usage.
        axis_death_dict = {}
        allied_death_dict = {}
        axis_wins_dict = {}
        allied_wins_dict = {}

        # Loop through the map-list and generate the dicts + messages.
        for idx, element in enumerate(map_list, 1):
            map_url = "http://46.101.44.19/maps/" + element + "/summary/"
            map_data = urllib.request.urlopen(map_url)
            map_data_contents = map_data.read()
            load_map_data = json.loads(map_data_contents)

            axis_deaths = int(load_map_data["axis_deaths"])
            allied_deaths = int(load_map_data["allied_deaths"])
            axis_wins = int(load_map_data["axis_wins"])
            allied_wins = int(load_map_data["allied_wins"])

            axis_death_dict[idx] = axis_deaths
            allied_death_dict[idx] = allied_deaths
            axis_wins_dict[idx] = axis_wins
            allied_wins_dict[idx] = allied_wins
 
        number_line = ["«", "-", "-", "-", "-",
                       "-", "-", "-", "-", "-",
                       "-", "-", "-", "-", "-",
                       "-", "-", "-", "-", "-",
                       "»"]       

        axis_wins_sum = sum(axis_wins_dict.values())
        allied_wins_sum = sum(allied_wins_dict.values())

        if axis_wins_sum > allied_wins_sum:
            rough_percentile = axis_wins_sum / (axis_wins_sum + allied_wins_sum)
            win_percentage = round(rough_percentile, 2)

            marker_shift = 20 * win_percentage

            marker_position = 20 - marker_shift
            number_line.insert(int(marker_position), "o")
            win_infographic = ''.join(number_line)
        elif axis_wins_sum < allied_wins_sum:
            rough_percentile = allied_wins_sum / (axis_wins_sum + allied_wins_sum)
            win_percentage = round(rough_percentile, 2)

            marker_shift = 20 * win_percentage

            number_line.insert(int(marker_shift), "o")
            win_infographic = ''.join(number_line)
        
        total_axis_deaths = "**Axis Deaths:** " + str(sum(axis_death_dict.values())) + " "
        total_allied_deaths = "| **Allied Deaths:** " + str(sum(allied_death_dict.values()))
        total_axis_wins = "| **Axis Wins:** " + str(axis_wins_sum) + "  "
        total_allied_wins = "  **Allied Wins:** " + str(allied_wins_sum) + " "

        wareffort_message = total_axis_deaths + total_axis_wins + win_infographic + total_allied_wins + total_allied_deaths

        await message.channel.send(wareffort_message)
    

    # -------------------------------------------------------------------------------------------------------
    # SERVER-POP SECTION
    # This section fetches server population data for displaying current server-population easily in discord.
    # This uses web-scraping on the gametracker DH webpage, as the darklight games API does not provide this
    # and gametracker is the only website I know of that has currently working server lists for DH.
    # -------------------------------------------------------------------------------------------------------
    elif "!servers" in message.content.lower():
        # Parse the DH gametracker page HTML.
        gametracker_url = "https://www.gametracker.com/search/rordh/"
        gametracker_raw = requests.get(gametracker_url)

        soup = BeautifulSoup(gametracker_raw.content, "html.parser")

        table = soup.find("table", attrs={"class":"table_lst table_lst_srs"})
        rows = table.find_all("tr")

        # Format the official DH servers into a list.
        table_data = []
        for td in rows[1].find_all("td"):
            table_data.append(td.text.strip())
        for td in rows[2].find_all("td"):
            table_data.append(td.text.strip())
        for td in rows[3].find_all("td"):
            table_data.append(td.text.strip())
        
        # Format the data we want (server name, pop, map) into a new list for printing.
        formatted_table = [[table_data[2], table_data[3], table_data[7]],
                           [table_data[10], table_data[11], table_data[15]],
                           [table_data[18], table_data[19], table_data[23]]
        ]

        formatted_output = tabulate(formatted_table, tablefmt="plain")

        await message.channel.send("```" + formatted_output + "```")

    elif "!commands" in message.content.lower():
        await message.channel.send("`!addme [ROID] - Adds you to the bot's database. 1-time command.`")
        await message.channel.send("`!stats - Displays your kills, deaths, and other common stats.`")
        await message.channel.send("`!ffstats - Displays your friendly-fire stats.`")
        await message.channel.send("`!map stats [map_name] - Displays the stats relating to a specific map.`")
        await message.channel.send("`!wareffort - Displays the total overall statistical progress of the war.`")


client.run(TOKEN)