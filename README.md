# DH-Statsbot
My Discord bot designed to display stats to users from the game Darkest Hour Europe.

The stats bot simply requires a user to provide their ROID along with the '!addme' command.
The bot then creates a new text file in the Users/ directory using their discord ID as the name.

The text files are arranged like so:

[Discord ID]

[ROID]

Some text files will also feature a username at the top, which is a remnant of a previous version that used to print usernames to the text file. I removed this as it was causing problems when users with emojis in their names attempted to add themselves to the bot. A user can be found by their discord ID by searching 'From: [ID]' in the discord search bar.

This is a one-time command and the user does not have to do it ever again. The bot will refer to this file whenever the '!stats' command is written in the discord #statistics channel. The bot refers to a stats website to get it's user information using the provided roid.
