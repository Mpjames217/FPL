import requests
from pprint import pprint
from operator import itemgetter

#Pull down info about team - including available transfers
max_transfers = 5
team_id = '8035167'
current_GW = '1' #fetch this from API
address = 'https://fantasy.premierleague.com/api/entry/' + team_id + '/event/' + current_GW + '/picks'
team_info = requests.get(address).json()

#Get full info on players in squad and count players per club
r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static').json()
all_players = r['elements']

squad_players = {1: [], 2: [], 3: [], 4: []}
all_squad_players = []

for player in all_players:
    for squad_player in team_info['picks']:
        if player['id'] == squad_player['element']:
            player['position'] = squad_player['position']
            player['form'] = float(player['form'])
            if player['chance_of_playing_next_round'] == 0:
                player['form'] = 0
            all_squad_players.append(player)
            squad_players[player['element_type']].append(player)

#select captain and vice captain
all_squad_players = sorted(all_squad_players, key=itemgetter('form'), reverse=True)
captain = all_squad_players[0]['web_name']
vice_captain = all_squad_players[1]['web_name']

#choose starting XI
#create list of formations
formations = [[1,5,4,1],[1,5,3,2],[1,4,4,2],[1,4,3,3],[1,3,5,2],[1,3,4,3]]
line_ups = {}
for formation in formations:
    line_ups[str(formation)] = {'starting_XI': [], 'total_form': 0}
    for i in range(len(formation)): #for each position
        for j in range(formation[i]): #for each slot in position
            line_ups[str(formation)]['starting_XI'].append(squad_players[i + 1][j]['web_name'])
            line_ups[str(formation)]['total_form'] += squad_players[i + 1][j]['form']

formation = ''
starting_XI = []
total_form = 0

for line_up in line_ups:
    if line_ups[line_up]['total_form'] > total_form:
        total_form = line_ups[line_up]['total_form']
        formation = line_up
        starting_XI = line_ups[line_up]['starting_XI']     

print(formation)
print(starting_XI)
print(captain)
print(vice_captain)
