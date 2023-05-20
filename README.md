[![Coverage Status](https://coveralls.io/repos/github/n-budzinski/Bastet/badge.svg?branch=main)](https://coveralls.io/github/n-budzinski/Bastet?branch=main)
# Bastet - Alexander Anubis emulator

A simple PoC master server emulator for GSC's Alexander (anubis.2gw.net).

<br />
<br />

### ***Server blocks ports required by the game. Use the built-in lan mode to play on the local machine.***

<br />
<br />

# Requirements

- A self hosted IRC server (in-game chat)

<br />

# Dependencies

- None

<br />

# Usage

 - Set up a local IRC server and change the settings.json accordingly.
 - Replace the GGW servers in [GAME_DIR]/Data/Internet/**ggwdc.ini**:

        #################################################################
        # This is configuration file for GSC Game World client software #
        ################################################################# 
        # Address of the GGW server
        ggwdserver_addr_1 your.alexander.server
        ggwdserver_addr_2 your.alexander.server
        ggwdserver_addr_3 your.alexander.server
        # Port of the GGW server
        ggwdserver_port 34001
        # Language/Locale to communicate with GGW server
        ggwdserver_lang 0
        # Protocol/Game version to communicate with GGW server
        ggwdserver_vers 16
- Run via main.py.

<br />

<br />

# Disclaimer

I am not affiliated, associated, authorized, endorsed by, or in any way officially connected with the GSC, Ubisoft, or any of its subsidiaries or its affiliates.
