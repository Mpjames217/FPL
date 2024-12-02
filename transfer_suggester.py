import requests
from pprint import pprint
from operator import itemgetter
from copy import deepcopy
import team_selector_function

#make calculate predicted points into function?
#Next steps: take into acount Double Gameweeks (DGWs), consider more than one transfer, combine with team_selector to factor in increase in first XI points?
#Maybe do one transfer by biggest form gain and only do multiple if improves first XI total points?

#Pull down data from API
r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static').json()
if type(r) == 'str':
    print(r)
    exit()
all_players = r['elements']

#find current gameweek
for gw in r['events']:
    if gw['is_current'] == True:
        current_GW = str(gw['id'])
        break

#team specific API call
team_id = '8035167'
address = 'https://fantasy.premierleague.com/api/entry/' + team_id + '/event/' + current_GW + '/picks'
team_info = requests.get(address).json()
transfer_budget = team_info['entry_history']['bank']

#initiate clubs dictionary
#To minimize number of API calls, will find one player from each club and record the Ficture Difficulty rating (FDR) for the club to be cross-referenced with later
clubs = {}
for i in range(1,21):
    clubs[i] = {'count': 0, 'average_FDR': 0}
    #get club FDR
    for player in all_players:
        if player['team'] == i:
            element_summary = requests.get('https://fantasy.premierleague.com/api/element-summary/' + str(player['id'])).json()
            clubs[i]['average_FDR'] = (element_summary['fixtures'][0]['difficulty'] + element_summary['fixtures'][1]['difficulty'] + element_summary['fixtures'][2]['difficulty']) / 3
            clubs[i]['next_match_FDR'] = element_summary['fixtures'][0]['difficulty']
            break

#get full information on  players in the squad and compile list of form players for each position

squad_players = [] # could compile seperate list of starters and bench players
form_players = []

for player in all_players:
    #calculate predicted points
    average_FDR = clubs[player['team']]['average_FDR']
    player['form'] = float(player['form'])
    if player['form'] > 0:
        player['predicted_points'] = player['form']/ average_FDR
    else:
        player['predicted_points'] = player['form'] * average_FDR
    if player['chance_of_playing_next_round'] != None:
        player['predicted_points'] *= (player['chance_of_playing_next_round']/ 100)
    #append squad players
    for squad_player in team_info['picks']:
        if player['id'] == squad_player['element']:
            squad_players.append(player)
            clubs[player['team']]['count'] += 1
    #append form players
    if player['form_rank_type'] < 10 and player not in squad_players and player['chance_of_playing_next_round'] != 0:
        form_players.append(player)

#make a list of possible transfers where predicted point delta exceeds 2
possible_transfers = []
transfer_elements = []

for form_player in form_players:
    for squad_player in squad_players:
        if form_player['element_type'] == squad_player['element_type'] and form_player['predicted_points'] > squad_player['predicted_points'] + 2 and form_player['now_cost'] <= squad_player['now_cost'] + transfer_budget:
            #check max players per club not exceeded
            if clubs[form_player['team']]['count'] < 3 or form_player['team'] == squad_player['team']:
                pp_delta = round(form_player['predicted_points'] - squad_player['predicted_points'], 2)
                possible_transfers.append({'player_in': form_player['web_name'], 'player_out': squad_player['web_name'], 'pp_delta': pp_delta})


#order transfers by point_delta
possible_transfers = sorted(possible_transfers, key=itemgetter('pp_delta'), reverse=True)

#inspect up to the top 20 transfers
n_transfers = 20
if len(possible_transfers) < n_transfers:
    n_transfers = len(possible_transfers)

line_ups = []

for i in range(n_transfers):
    print(possible_transfers[i])

    temp_squad_players = deepcopy(squad_players)

    for j in range(len(temp_squad_players)):
        player = temp_squad_players[j]
        if player['web_name'] == possible_transfers[i]['player_out']:
            for form_player in form_players:
                if form_player['web_name'] == possible_transfers[i]['player_in']:
                    temp_squad_players[j] = form_player
            
    line_up = team_selector_function.team_selector(temp_squad_players, clubs, 'average_FDR')
    # print(line_up)
    line_up['squad'] = temp_squad_players
    line_up['transfer'] = possible_transfers[i]
    line_ups.append(line_up)

line_ups = sorted(line_ups, key=itemgetter('total_predicted_points'), reverse=True)
current_gw_line_up = team_selector_function.team_selector(line_ups[0]['squad'], clubs, 'next_match_FDR')
current_gw_line_up['total_predicted_points'] = round(current_gw_line_up['total_predicted_points'])

print(line_ups[0]['transfer'])
pprint(current_gw_line_up)
