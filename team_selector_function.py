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
                if player['chance_of_playing_next_round'] == 0:
                    player['predicted_points'] = 0
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

    return line_ups[0]
