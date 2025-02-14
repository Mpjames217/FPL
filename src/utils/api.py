import requests, asyncio, aiohttp, pprint

def get_data(address):
    try:
        response = requests.get(address).json()
        if isinstance(response, str):
            print(response)
            exit()
        else:
            return response
    except:
        print('Error encounted accessing API. Execution will terminate')
        exit()

def get_current_gw(response):
    for gw in response['events']:
        if gw['is_current'] == True:
            return str(gw['id'])
        
async def get_fixtures_by_player(player_id, session, current_gw):
    url = 'https://fantasy.premierleague.com/api/element-summary/' + str(player_id)
    next_gw = int(current_gw) + 1
    async with session.get(url) as response:
        element_summary = await response.json()
        fixtures = {}
        for gw in range(next_gw, next_gw + 3):
            fixtures[gw] = []
            for fixture in element_summary['fixtures']:
                if fixture['event'] == gw:
                    fixtures[gw].append(fixture['difficulty'])
        return fixtures


async def get_FDR_by_club(all_players, current_gw):
    #get club FDR - upcoming fixtures only availble on player specific endpoints so making a call of one player per club
    player_ids = []
    for i in range(1,21):
        for player in all_players:
            if player['team'] == i:
                player_ids.append(player['id'])
                break
    
    async with aiohttp.ClientSession() as session:
        tasks = [get_fixtures_by_player(id, session, current_gw) for id in player_ids]
        response = await asyncio.gather(*tasks)
    
    fixtures = {}
    for i in range(1,21):
        fixtures[i] = response[i-1]

    pprint.pprint(fixtures)
    return fixtures
