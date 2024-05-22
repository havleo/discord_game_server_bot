#!/bin/bash

pkill python3

# Start new
export DISCORD_TOKEN=$(gpg --decrypt token.gpg)
nohup bash -c "python3 game_server_bot.py" > out &
unset DISCORD_TOKEN
