# This file contains the code necessary for fetching the current playercount.
# The bot's status message updates with the total playercount
# and users can use a command to view playercount on individual servers.
import requests
import urllib.request
from bs4 import BeautifulSoup
from tabulate  import tabulate

# Ping the gametracker webpage for server-info.
def pingServers():
    gametracker_url = "https://www.gametracker.com/search/rordh/"
    gametracker_raw = requests.get(gametracker_url)

    soup = BeautifulSoup(gametracker_raw.content, "html.parser")

    table = soup.find("table", attrs={"class":"table_lst table_lst_srs"})
    rows = table.find_all("tr")

    table_data = []
    for td in rows[1].find_all("td"):
        table_data.append(td.text.strip())
    for td in rows[2].find_all("td"):
        table_data.append(td.text.strip())
    for td in rows[3].find_all("td"):
        table_data.append(td.text.strip())
    for td in rows[4].find_all("td"):
        table_data.append(td.text.strip())
    for td in rows[5].find_all("td"):
        table_data.append(td.text.strip())

    return table_data


# Update the bot's status message with the total playercount.
def statusUpdate():
    table_data = pingServers()

    # Extract the playercount integers from table_data.
    count_1 = table_data[3]
    count_2 = table_data[11]
    count_3 = table_data[19]
    count_4 = table_data[27]
    count_5 = table_data[35]

    # Cut-off the uneeded "/64" part.
    component_1 = str(count_1[:-3])
    component_2 = str(count_2[:-3])
    component_3 = str(count_3[:-3])
    component_4 = str(count_4[:-3])
    component_5 = str(count_5[:-3])

    total_playercount = int(component_1) + int(component_2) + int(component_3) + int(component_4) + int(component_5)

    status_message = str(total_playercount) + " players playing"

    return status_message


# Return a formatted table of server playercount to be printed to Discord.
def serverList():
    table_data = pingServers()
    
    # Format the data we want (server name, pop, map) into a new list for printing.
    formatted_table = [[table_data[2], table_data[3], table_data[7]],
                        [table_data[10], table_data[11], table_data[15]],
                        [table_data[18], table_data[19], table_data[23]],
                        [table_data[26], table_data[27], table_data[31]],
                        [table_data[34], table_data[35], table_data[39]]
    ]

    formatted_output = tabulate(formatted_table, tablefmt="plain")

    return formatted_output
