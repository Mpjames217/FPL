from operator import itemgetter
from copy import deepcopy
from src.team_selector import team_selector

def sort_transfers_by_first_xi_impact(possible_transfers, squad_players, form_players):
    ''' Takes a list of possible transfers
        returns a list of the line ups for up to 10 transfers, sorted by the total points of the starting xi'''
    n_transfers = 10
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
                
        line_up = team_selector(temp_squad_players)
        line_up['squad'] = temp_squad_players
        line_up['transfer'] = possible_transfers[i]
        line_ups.append(line_up)

    return  sorted(line_ups, key=itemgetter('total_predicted_points'), reverse=True)