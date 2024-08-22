import requests, json
from pprint import pprint
from operator import itemgetter
#use form as metric for now

#Pull down info about team - including available transfers
max_transfers = 5
team_id = '8035167'
current_GW = '1' #fetch this from API
address = 'https://fantasy.premierleague.com/api/entry/' + team_id + '/event/' + current_GW + '/picks'
team_info = requests.get(address).json()

#Get full info on players in squad and count players per club
r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static').json()
all_players = r['elements']
squad_players = [] # could compile seperate list of starters and bench players

#initiate club counter dictionary
clubs = {}
for i in range(1,21):
    clubs[i] = 0

for player in all_players:
    for squad_player in team_info['picks']:
        if player['id'] == squad_player['element']:
            squad_players.append(player)
            clubs[player['team']] += 1


#get top players by form for each position - exluding players already in team and players with injuries

form_players = []
for player in all_players:
    if player['form_rank_type'] < 10 and player not in squad_players and player['chance_of_playing_next_round'] != 0:
        form_players.append(player)

#make a list of possible transfers if there is a positive form delta
possible_transfers = []

for form_player in form_players:
    for squad_player in squad_players:
        if form_player['element_type'] == squad_player['element_type'] and float(form_player['form']) > float(squad_player['form']) + 2 and form_player['now_cost'] <= squad_player['now_cost']:
            #check max players per club not exceeded
            if clubs[form_player['team']] < 3 or form_player['team'] == squad_player['team']:
                possible_transfers.append({'player_in': form_player['web_name'], 'player_out': squad_player['web_name'], 'form_delta': float(form_player['form']) - float(squad_player['form'])})

#order transfers by point_delta
possible_transfers = sorted(possible_transfers, key=itemgetter('form_delta'), reverse=True)

pprint(possible_transfers)