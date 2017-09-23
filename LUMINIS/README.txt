This file will briefly explain the file and directory structure of the game.

TL;DR:
	Put your AI in a subdirectory of the "Bots" directory.

	If you want to run a game (between AI or using an IDE), you can start up the launcher by running:
		- "Launcher.bat" on Windows
		- "Launcher.sh" on OS X and Linux


Bots
----

Your AI goes here! You should put it in a subdirectory, like Bots/GladiatorBot
The subdirectory name will be used as your AI's name.

Libraries
---------

The game's binary files are located here, along with the Python Client. If you want to set up an IDE,
this is where you find the files you need to run your client.

Logs
----

Output logs from the server and the clients are stored here.
Client logs are logged to the launcher's client monitor window too,
and server logs will be logged to the terminal window you run the launcher from.

Manual
------
This contains the game manual in HTML format.
It outlines everything you'll need to get started, from IDE configuration to game rules.
Double-click Manual/index.html to read the manual :)

Maps
----

This directory contains map files and their navigation caches.
The navigation cache compiler is also located here.

See the manual for more information about navigation caches.

MatchPresets
------------

This directory contains match presets that can be configured and saved from the launcher UI.
It is strongly recommended they not be edited manually.

Resources
---------

The game's assets are located here. Changing or removing anything in this folder may cause the server to crash.

Results
-------

After each game, results are stored in this folder.
These files contain the final scores and their breakdowns, as well as a history of all the moves received by the server during each turn.


The Shell Scripts
-----------------

There are two shell scripts available to run the launcher.
The script ending in .bat is for Windows, while the one ending in .sh is for macOS and Linux.

If you want to run a game (between AI or using an IDE), you can start up the launcher by running:
		- "Launcher.bat" on Windows
		- "Launcher.sh" on OS X and Linux



Thanks for reading me! 

More information can be found in the manual :)
If you have any questions or concerns, please don't hesitate to get in touch with us!

Good luck!