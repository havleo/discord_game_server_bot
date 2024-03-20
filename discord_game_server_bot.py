import discord
import os

# Discord
intents = discord.Intents.default()

intents.message_content = True
intents.members = True

discord_client = discord.Client(intents=intents)

# Valheim
valheim_server_path = '/home/leo/lloesche/valheim-server'
valheim_members= {
    'Mbutu': 'Rac',
    'Mutimir': 'mutimir',
    'JaDrankaKosor': 'ditecacino',
    'Yugonord': 'lecika',
    'Josko': 'fulir',
    'Tec': 'malipajdo',
    'Yeo': 'yeo3130'
}

def start_valheim_server():
    os.chdir(valheim_server_path)
    os.system('docker compose up -d')

def stop_valheim_server():
    os.chdir(valheim_server_path)
    os.system('docker compose down')

async def recogniseRole(message, targetRole, recognition):
    name = valheim_members[message.content.split()[0]]
    member = message.guild.get_member_named(name)
    for role in member.roles:
        if role.name in targetRole: 
            await message.channel.send(recognition + ' ' + member.mention)
            break

async def recogniseEnter(message):
    await recogniseRole(message, 'SailingMaster', 'Vjetar u leđa kapetane')
    await recogniseRole(message, 'FishingMaster', 'Debele ribe te čekaju')
    await recogniseRole(message, 'Arhitekta', 'Nema dosta kamenja')

async def recogniseLeave(message):
    await recogniseRole(message, 'SailingMaster', 'Kapetan tone s brodom')
    await recogniseRole(message, 'FishingMaster', 'Tolika je bila riba, al je utekla')
    await recogniseRole(message, 'Arhitekta', 'Sad je još manje kamenja')



# Discord Events
@discord_client.event
async def on_ready():
    print(f'We have logged in as {discord_client.user}')

@discord_client.event
async def on_message(message):
    try:
        if message.author == discord_client.user:
            return

        if message.content.startswith('$valheim_start'):
            await message.channel.send("Starting Valheim server...")
            start_valheim_server()
        if message.content.startswith('$valheim_stop'):
            await message.channel.send("Stopping Valheim server...")
            stop_valheim_server()
        if message.content.endswith('has joined.'):
            await recogniseEnter(message)
        if message.content.endswith('has left.'):
            await recogniseLeave(message)
    except Exception as error:
        await message.channel.send("Something went wrong, error: {}".format(error))

# Start the bot
print(os.environ['DISCORD_TOKEN'])
discord_client.run(os.environ['DISCORD_TOKEN'])
