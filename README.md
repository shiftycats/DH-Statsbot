# DH-Statsbot
My Discord bot designed to display stats to users from the game Darkest Hour Europe.

The stats bot simply requires a user to provide their ROID along with the '!addme' command.
The bot then creates a new entry to the "users.txt" file with their Discord ID and their ROID. This is stored and used as a reference to get the player's stats from the stats website - http://stats.darklightgames.com/

The user-entries are arranged like so: [Discord ID] [ROID]

A user can be found by their discord ID by searching 'From: [ID]' in the discord search bar.

This is a one-time command and the user does not have to do it ever again. The bot will refer to this file whenever the '!stats' command is written in the discord #statistics channel.

TODO: (Finished features will be crossed-out)
* ~~Rewrite the user-handling system so everything is written into one file instead of many seperate files.~~
* Basic leaderboard commands for each stat. Eg. "Most Kills", "Most Deaths", etc.
* A command to display to the user their most-killed player / vice-versa.
* ~~Display a player's favorite (most kills) weapon in the stats command.~~
