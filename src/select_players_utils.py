from itertools import combinations
from operator import itemgetter
from pprint import pprint

def get_club_count(players):
    club_count = {i:0 for i in range(1,21)}
    for player in players:
        club = player['club']
        club_count[club] += 1
    return club_count

def get_players_cost(players):
    cost = 0
    for player in players:
        cost += player['cost']
    return cost

def get_total_points(players):
    total_points = 0
    for player in players:
        total_points += player['points']
    return total_points

def get_top_player_combinations(players, slots, n_results):
    player_combinations = combinations(players, slots)

    top_player_combinations = []
    for line_up in player_combinations:
        temp_dict = {}
        # temp_dict['club_count'] = get_club_count(line_up)
        temp_dict['players'] = line_up
        temp_dict['points'] = get_total_points(line_up)
        temp_dict['cost'] = get_players_cost(line_up)

        top_player_combinations.append(temp_dict)


    top_player_combinations = sorted(top_player_combinations, key=itemgetter('points'), reverse=True)
    top_player_combinations = top_player_combinations[0:n_results]
    
    return top_player_combinations

def get_starting_xi(top_gks, top_defences, top_midfields, top_forwards, budget):
    top_player_combinations = []
    for gk in top_gks:
        for defence in top_defences:
            for midfield in top_midfields:
                for forward in top_forwards:
                    starting_xi = gk['players'] + defence['players'] + midfield['players'] + forward['players']

                    temp_dict = {}
                    temp_dict['club_count'] = get_club_count(starting_xi)
                    temp_dict['players'] = starting_xi
                    temp_dict['points'] = get_total_points(starting_xi)
                    temp_dict['cost'] = get_players_cost(starting_xi)

                    if temp_dict['cost'] < budget:
                        top_player_combinations.append(temp_dict)


    top_player_combinations = sorted(top_player_combinations, key=itemgetter('points'), reverse=True)
    top_player_combinations = top_player_combinations[0:5]
    # pprint(top_player_combinations)
    
    return top_player_combinations[0]