import requests
from pprint import pprint
from operator import itemgetter

#Pull down info about team
team_id = '8035167'
current_GW = '3' #fetch this from API
address = 'https://fantasy.premierleague.com/api/entry/' + team_id + '/event/' + current_GW + '/picks'
team_info = requests.get(address).json()

#Get full info on players in squad and count players per club
r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static').json()
if r == 'The game is being updated.':
    print(r)
    exit()

all_players = r['elements']

squad_players = {1: [], 2: [], 3: [], 4: []}
all_squad_players = []

for player in all_players:
    for squad_player in team_info['picks']:
        if player['id'] == squad_player['element']:
            #get FDR of players next match
            element_summary = requests.get('https://fantasy.premierleague.com/api/element-summary/' + str(player['id'])).json()
            FDR = element_summary['fixtures'][0]['difficulty']
            modified_FDR = 1 + FDR / 10
            #add extra feilds and append to all_squad_players
            player['predicted_points'] = float(player['form'])  / modified_FDR
            if player['chance_of_playing_next_round'] == 0:
                player['predicted_points'] = 0
            player['position'] = squad_player['position']
            all_squad_players.append(player)
            squad_players[player['element_type']].append(player)

#select captain and vice captain
all_squad_players = sorted(all_squad_players, key=itemgetter('predicted_points'), reverse=True)
captain = all_squad_players[0]['web_name']
vice_captain = all_squad_players[1]['web_name']

#choose formation and starting XI based on predicted points

formations = [[1,5,4,1],[1,5,3,2],[1,4,4,2],[1,4,3,3],[1,3,5,2],[1,3,4,3]]

for position in squad_players:
    squad_players[position] = sorted(squad_players[position], key=itemgetter('predicted_points'), reverse=True)

line_ups = {}
for formation in formations:
    line_ups[str(formation)] = {'starting_XI': [], 'total_predicted_points': 0}
    for i in range(len(formation)): #for each position
        for j in range(formation[i]): #for each slot in position
            line_ups[str(formation)]['starting_XI'].append(squad_players[i + 1][j]['web_name'])
            line_ups[str(formation)]['total_predicted_points'] += squad_players[i + 1][j]['predicted_points']


formation = ''
starting_XI = []
total_predicted_points = 0

for line_up in line_ups:
    if line_ups[line_up]['total_predicted_points'] > total_predicted_points:
        total_predicted_points = line_ups[line_up]['total_predicted_points']
        formation = line_up
        starting_XI = line_ups[line_up]['starting_XI']

print(formation)
print(starting_XI)
print('Captain: ' + captain)
print('Vice Captain: ' + vice_captain)