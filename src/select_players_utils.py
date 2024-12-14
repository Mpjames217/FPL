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
    
    return top_player_combinations[0]

def get_bench_players(bench_positions, all_player_data):
    bench_players = {}
    for position in bench_positions:
        if bench_positions[position] > 0:
            bench_players[position] = []

    bench_budgets = {}
    bench_budgets['GK']  = 4.0
    bench_budgets['DEF'] = 4.0
    bench_budgets['MID'] = 4.5
    bench_budgets['FWD'] = 4.5

    #select best players at lowest price piont for each empty position where player per team limit is not exceeded
    #determine bench order - order by average predicted pionts/value or by enforced substitutions?
    for position in bench_players:
        for slot in range(bench_positions[position]):
            slot_budget = bench_budgets[position]
            for player in all_player_data[position]:
                #check player eligable: under budget, players per club not exceeded, not already in list
                if player['cost'] <= slot_budget and player not in bench_players[position]:
                    #if slots for position not full
                    if len(bench_players[position]) < bench_positions[position] and player not in bench_players[position]:
                        bench_players[position].append(player)
                    #otherwise, check for better scoring players
                    else:
                        if player['points'] > bench_players[position][slot]['points']:
                            bench_players[position][slot] = player

    return bench_players