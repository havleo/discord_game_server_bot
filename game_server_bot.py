import discord
import os
import sys

# Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
discord_client = discord.Client(intents=intents)

# Valheim config
valheim_server_path = '/home/leo/valheim'
valheim_members = {
    'Mbutu': 'Rac',
    'Mutimir': 'mutimir',
    'JaDrankaKosor': 'ditecacino',
    'Yugonord': 'lecika',
    'Josko': 'fulir',
    'Tec': 'malipajdo',
    'Yeo': 'yeo3130'
}

# VRising config
launch_code_timeout = 20
vrising_server_path = '/home/leo/vrising'


# Recognition
async def recogniseRole(message, targetRole, recognition):
    name = valheim_members[message.content.split()[0]]
    member = message.guild.get_member_named(name)
    for role in member.roles:
        if role.name in targetRole: 
            await message.channel.send(recognition + ' ' + member.mention)
            break

# Discord Events
@discord_client.event
async def on_message(message):
    try:
        if message.author == discord_client.user:
            return

        if '$valheim_start' in message.content:
            await message.channel.send("Starting Valheim server...")
            os.chdir(valheim_server_path)
            os.system('docker compose up -d')

        elif '$valheim_stop' in message.content:
            await message.channel.send("Stopping Valheim server...")
            os.chdir(valheim_server_path)
            os.system('docker compose down')

        elif '$vrising_start' in message.content:
            await message.channel.send("Starting VRising server...")
            os.chdir(vrising_server_path)
            os.system('docker compose up -d')
            await message.channel.send("Pokrenuo se, traje oko minutu da proradi...")

        elif '$vrising_stop' in message.content:
            await message.channel.send("Stopping VRising server...")
            os.chdir(vrising_server_path)
            os.system('docker compose down')

        elif 'has joined.' in message.content:
            await recogniseRole(message, 'SailingMaster', 'Vjetar u leđa kapetane')
            await recogniseRole(message, 'FishingMaster', 'Debele ribe te čekaju')
            await recogniseRole(message, 'Arhitekta', 'Nema dosta kamenja')

        elif 'has left.' in message.content:
            await recogniseRole(message, 'SailingMaster', 'Kapetan tone s brodom')
            await recogniseRole(message, 'FishingMaster', 'Tolika je bila riba, al je utekla')
            await recogniseRole(message, 'Arhitekta', 'Sad je još manje kamenja')

        else:
            return
    except Exception as error:
        await message.channel.send("Something went wrong, error: {}".format(error))

# Start the bot
discord_client.run(os.environ['DISCORD_TOKEN'])
