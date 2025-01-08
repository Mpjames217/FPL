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
        
async def get_element_summaries(player_id, session):
    url = 'https://fantasy.premierleague.com/api/element-summary/' + str(player_id)
    async with session.get(url) as response:
        element_summary = await response.json()
        FDR_next_match = element_summary['fixtures'][0]['difficulty']
        FDR_average = (element_summary['fixtures'][0]['difficulty'] + element_summary['fixtures'][1]['difficulty'] + element_summary['fixtures'][2]['difficulty']) / 3
        return FDR_next_match , FDR_average


async def get_FDR_by_club(all_players):
    #get club FDR - upcoming fixtures only availble on player specific endpoints so making a call of one player per club
    player_ids = []
    for i in range(1,21):
        for player in all_players:
            if player['team'] == i:
                player_ids.append(player['id'])
                break
    
    async with aiohttp.ClientSession() as session:
        tasks = [get_element_summaries(id, session) for id in player_ids]
        response = await asyncio.gather(*tasks)
    
    FDR_next_match = {}
    FDR_average = {}
    for i in range(1,21):
        FDR_next_match[i] = response[i-1][0]
        FDR_average[i] = response[i-1][1]

    return FDR_next_match, FDR_average