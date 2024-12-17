import requests
from pprint import pprint
from operator import itemgetter

def team_selector(squad_players, clubs, FDR_type):  

    squad_players_by_position = {1: [], 2: [], 3: [], 4: []}

    for player in squad_players:
                #Modify predicted points based on Fixture Difficulty Rating (FDR) of players next match only
                FDR = clubs[player['team']][FDR_type]
                #FDR is altered to make a more appropriate modifier for form. 2 is deducted from the avg as 2 is the baseline difficulty
                modified_FDR = 1 + (FDR - 2) / 10
                #add extra feilds and append to all_squad_players
                player['predicted_points'] = float(player['form'])  / modified_FDR
                if player['chance_of_playing_next_round'] != None:
                    player['predicted_points'] *= (player['chance_of_playing_next_round']/ 100)
                squad_players_by_position[player['element_type']].append(player)

    #choose formation and starting XI based on predicted points
    formations = [[1,5,4,1],[1,5,3,2],[1,4,4,2],[1,4,3,3],[1,3,5,2],[1,3,4,3]]

    for position in squad_players_by_position:
        squad_players_by_position[position] = sorted(squad_players_by_position[position], key=itemgetter('predicted_points'), reverse=True)

    #add up the predicted points for the best 11 players in each formation
    line_ups = []
    for formation in range(len(formations)):
        line_ups.append({'formation': formations[formation], 'starting_XI': [], 'total_predicted_points': 0})
        for i in range(len(formations[formation])): #for each position
            for j in range(formations[formation][i]): #for each slot in position
                line_ups[formation]['starting_XI'].append(squad_players_by_position[i + 1][j]['web_name'])
                line_ups[formation]['total_predicted_points'] += squad_players_by_position[i + 1][j]['predicted_points']


    line_ups = sorted(line_ups, key=itemgetter('total_predicted_points'), reverse=True)
    line_up = line_ups[0]
    
    #select captain and vice captain
    squad_players = sorted(squad_players, key=itemgetter('predicted_points'), reverse=True)
    captain = squad_players[0]['web_name']
    captain_points = squad_players[0]['predicted_points']
    vice_captain = squad_players[1]['web_name']

    line_up['total_predicted_points'] += captain_points
    line_up['total_predicted_points'] = round(line_up['total_predicted_points'])
    line_up['Captain'] = captain
    line_up['Vice Captain'] = vice_captain

    return line_up

if __name__ == "__main__":
    #Get full info on players in squad and count players per club
    r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static').json()
    if r == 'The game is being updated.':
        print(r)
        exit()

    all_players = r['elements']

    #find current gameweek
    for gw in r['events']:
        if gw['is_current'] == True:
            current_GW = str(gw['id'])
            break

    #Pull down info about team
    team_id = '8035167'
    address = 'https://fantasy.premierleague.com/api/entry/' + team_id + '/event/' + current_GW + '/picks'
    team_info = requests.get(address).json()

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


    squad_players = []

    for player in all_players:
        for squad_player in team_info['picks']:
            if player['id'] == squad_player['element']:
                #get Fixture Difficulty Rating (FDR) of players next match
                element_summary = requests.get('https://fantasy.premierleague.com/api/element-summary/' + str(player['id'])).json()
                FDR = element_summary['fixtures'][0]['difficulty']
                #FDR is altered to make a more appropriate modifier for form. 2 is deducted from the avg as 2 is the baseline difficulty
                modified_FDR = 1 + (FDR - 2) / 10
                #add extra feilds and append to squad_players
                if float(player['form']) < 0:
                    player['predicted_points'] = float(player['form']) * modified_FDR
                else:
                    player['predicted_points'] = float(player['form']) / modified_FDR
                if player['chance_of_playing_next_round'] == 0:
                    player['predicted_points'] = 0
                player['position'] = squad_player['position']
                squad_players.append(player)



    pprint(team_selector(squad_players, clubs, 'next_match_FDR'))

