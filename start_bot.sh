#!/bin/bash

# Kill last proc
kill $(ps -ef | grep game_server_bot.py | grep -v grep --color=never | awk '{ printf "%s", $2 }')

# Start new
export DISCORD_TOKEN=$(gpg --decrypt token.gpg)
nohup python3 game_server_bot.py > disc_bot.out &
unset DISCORD_TOKEN
