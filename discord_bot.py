import nextcord, colorama, datetime, json, requests
from nextcord.ext import commands, tasks

colorama.init(autoreset=True)

intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)

@tasks.loop(minutes=10)
async def update_json():
    # The role you're checking for
    role_name = 'Admin'

    # The new JSON file to write to
    new_file = []

    # Set to keep track of discordIDs
    discord_ids = set()

    # Get the guild (server)
    guild = bot.guilds[0]  # If you have multiple servers, replace 0 with the index of the correct server

    # Load the LinkedPlayers.json file
    with open('DiscordIntegration-Data/LinkedPlayers.json', 'r') as f:
        linked_players = json.load(f)

    for player in linked_players:
        discord_id = player['discordID']
        if discord_id in discord_ids:
            continue
        member = await guild.fetch_member(discord_id)

        # Check if the member has the role
        if any(role.name == role_name for role in member.roles):
            # Make a GET request
            response = requests.get(f'https://playerdb.co/api/player/minecraft/{player["mcPlayerUUID"]}')
            # Check if the request was successful
            if response.status_code == 200:
                # Add the returned information to the new file
                player_info = response.json()
                username = player_info['data']['player']['username']
                new_file.append({
                    'discord_id': discord_id,
                    'mc_username': username
                })
                discord_ids.add(discord_id)
            else:
                print(f'Failed to get information for player {player["mcPlayerUUID"]}: {response.status_code}')

    # Write to the new JSON file
    with open('brass_players.json', 'w') as f:
        json.dump({'players': new_file}, f, indent=4)
    print(f'Updated FTB Ranks supporter ranks Json files updated at {datetime.datetime.now()}')

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.streaming, name='on top of the mountains'))
    global start_time
    start_time = datetime.datetime.now()
    print('\x1b[32;1m' + f'We have logged in as {bot.user} at {datetime.datetime.now()}')
    
    update_json.start()

    # Load the LinkedPlayers.json file
    with open('DiscordIntegration-Data/LinkedPlayers.json', 'r') as f:
        linked_players = json.load(f)

    # The role you're checking for
    role_name = 'Admin'

    # The new JSON file to write to
    new_file = []

    # Get the guild (server)
    guild = bot.guilds[0]  # If you have multiple servers, replace 0 with the index of the correct server

    for player in linked_players:
        discord_id = player['discordID']
        member = await guild.fetch_member(discord_id)

        # Check if the member has the role
        if any(role.name == role_name for role in member.roles):
            # Make a GET request
            response = requests.get(f'https://playerdb.co/api/player/minecraft/{player["mcPlayerUUID"]}')
            # Check if the request was successful
            if response.status_code == 200:
                # Add the returned information to the new file
                player_info = response.json()
                username = player_info['data']['player']['username']
                player_icon = player_info['data']['player']['avatar']
                new_file.append({
                    'discord_id': discord_id,
                    'mc_username': username
                })
            else:
                print(f'Failed to get information for player {player["mcPlayerUUID"]}: {response.status_code}')

    # Write to the new JSON file
    with open('brass_players.json', 'w') as f:
        json.dump({'players': new_file}, f, indent=4)



bot.run('MTE4OTM1NzA5OTQwMzE5ODYxNA.GPWJ5M.uNisFPcDbamr2ZmUK4UGgBidi4ZrDOLRgjDsaM')