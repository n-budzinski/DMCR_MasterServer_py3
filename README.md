# Bastet


A simple master server emulator for GSC's Alexander (anubis.2gw.net).

<br />

### *Server blocks ports required for hole punching - the game will not work properly on the system hosting the server!*

<br />
<br />
<br />

## Requirements

An IRC server used by the in-game comms. You can either host your own or use a public one.

Default IRC channels (rooms) used by the client:
- #GSP!conquest_m!5
- #GSP!conquest!3

<br />
<br />

## Issues

- Doesn't work with the demo version of the game.

<br />
<br />

## Getting started

 1. Change the variables in config.py accordingly.
 2. Replace the GGW servers in [Game's location]/Data/Internet/**ggwdc.ini**:

        #################################################################
        # This is configuration file for GSC Game World client software #
        ################################################################# 
        # Address of the GGW server
        ggwdserver_addr_1 [your.alexander.server]
        ggwdserver_addr_2 [your.alexander.server]
        ggwdserver_addr_3 [your.alexander.server]
        # Port of the GGW server
        ggwdserver_port 34001
        # Language/Locale to communicate with GGW server
        ggwdserver_lang 0
        # Protocol/Game version to communicate with GGW server
        ggwdserver_vers 16
 3. Run via main.py.

<br />
<br />

## Disclaimer

I am not affiliated, associated, authorized, endorsed by, or in any way officially connected with the GSC, Ubisoft, or any of its subsidiaries or its affiliates.
