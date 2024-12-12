from pprint import pprint
from datetime import datetime
import utils
import select_players_utils

all_player_data = utils.get_all_player_data()

all_player_data = utils.transform_all_player_data(all_player_data)

price_points = utils.get_unique_price_points(all_player_data)

top_players = utils.get_top_players_per_price_point(all_player_data, price_points, 1 )

#create list of formations
#formations = [[5,4,1],[5,3,2],[4,4,2],[4,3,3],[3,5,2],[3,4,3]]
formations = [[3,5,2]]

bench_budgets = {}
bench_budgets['GK']  = 4.0
bench_budgets['DEF'] = 4.0
bench_budgets['MID'] = 4.5
bench_budgets['FWD'] = 4.5


#initiate club counter dictionary
clubs = {i:0 for i in range(1,21)}

#declare variables for using in nested loops below
budget = 100

results = {'Points': 0, 'Starting_XI': [], 'Cost': budget, 'Bench': []}
combinations_tested = 0

#loop through each combination of players
for formation in formations:

    def_slots = formation[0]
    mid_slots = formation[1]
    fwd_slots = formation[2]

    bench_positions = {}
    bench_positions['GK'] = 1
    bench_positions['DEF'] = 5 - def_slots
    bench_positions['MID'] = 5 - mid_slots
    bench_positions['FWD'] = 3 - fwd_slots
    min_bench_budget = 0
    for position in bench_budgets:
        min_bench_budget += bench_budgets[position] * bench_positions[position]
    #And budget for starting XI
    starting_XI_budget = budget - min_bench_budget
    print(starting_XI_budget)

    n_combinations = 50

    top_GKs = select_players_utils.get_top_player_combinations(top_players['GK'], 1, n_combinations)
    top_defences = select_players_utils.get_top_player_combinations(top_players['DEF'], def_slots, n_combinations)
    top_midfields = select_players_utils.get_top_player_combinations(top_players['MID'], mid_slots, n_combinations)
    top_forwards = select_players_utils.get_top_player_combinations(top_players['FWD'], fwd_slots, n_combinations)
    # print(type(top_forwards))
    # pprint(top_forwards)

    results['Starting_XI'] = select_players_utils.get_starting_xi(top_GKs, top_defences, top_midfields, top_forwards, starting_XI_budget)

    





#fill bench

#create bench players data structure
bench_players = {}
for position in bench_positions:
    if bench_positions[position] > 0:
        bench_players[position] = []

#select best players at lowest price piont for each empty position where player per team limit is not exceeded
#determine bench order - order by average predicted pionts/value or by enforced substitutions?
for position in bench_players:
    for slot in range(bench_positions[position]):
        slot_budget = bench_budgets[position]
        for player in all_player_data[position]:
            #check player eligable: under budget, players per club not exceeded, not already in list
            if player['cost'] <= slot_budget and clubs[player['club']] < 3 and player not in bench_players[position]:
                #if slots for position not full
                if len(bench_players[position]) < bench_positions[position] and player not in bench_players[position]:
                    bench_players[position].append(player)
                #otherwise, check for better scoring players
                else:
                    if player['points'] > bench_players[position][slot]['points']:
                        bench_players[position][slot] = player

#create list of bench player names and add to results{}
for position in bench_players:
    for player in bench_players[position]:
        results['Bench'].append(player['name'])

#del results['Clubs']
pprint(results)