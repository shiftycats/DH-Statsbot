# DH-Statsbot

DH-Statsbot is my project to provide a simple-to-use and quick text interface that mirrors the statistics as seen on the official Darkest Hour stats website.

Typically every couple months I try to add a new feature to statsbot. As of now, March of 2021, statsbot has the following functional features:

* Personal statistic display (Kills, deaths, teamkills, kd/r, etc.)
* Server-pop display
* Individual map statistic display 
  * (Total deaths on a given map across all rounds, which side is "winning" overall between axis & allied powers on each map.)

* Overall "war-progress" display 
  * (Displays the total number of deaths that have occured and are recorded on the stats website, which faction is currently "winning.")
  * NOTE: This feature is currently disabled because it's very slow and the calculations for it block other commands from executing.

DISCLAIMER FOR USERS - Due to some unreliability with the Darklight Games stats website currently, user-stats are not 100% accurate. This is an issue that the Darklight Games developers are aware of and have stated will be fixed at some point in the future.

--

The current external modules used are:
* Discord.py
* BeautifulSoup
* Tabulate

I maintain and host statsbot on my computer for the Darkest Hour discord. No responsibility should fall to the DH developers or Darklight Games should statsbot stop working, this is all my personal project for the community.

Statsbot was my first real programming project. As a result, the quality of my code is all over the place, mainly in the gutter for 99% of it. I have thought about rewriting the entirety of statsbot in a different language like Rust, or just tearing it down and starting from scratch once again, but it works and it hasn't run into any slowdowns that I can tell as of yet, so I will continue adding to it for the time being. If you have any questions you can contact me mainly on Discord @Chaussettes#8027.
