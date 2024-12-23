import requests

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
        

def get_FDR_by_club(all_players):
    FDR_next_match = {}
    FDR_average = {}
    for i in range(1,21):
        #get club FDR - upcoming fictures only availble on player specific endpoints so making a call of one player per club
        for player in all_players:
            if player['team'] == i:
                element_summary = get_data('https://fantasy.premierleague.com/api/element-summary/' + str(player['id']))
                FDR_average[i] = (element_summary['fixtures'][0]['difficulty'] + element_summary['fixtures'][1]['difficulty'] + element_summary['fixtures'][2]['difficulty']) / 3
                FDR_next_match[i] = element_summary['fixtures'][0]['difficulty']
                break
    return FDR_next_match, FDR_average

