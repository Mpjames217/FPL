from pprint import pprint
from datetime import datetime
import utils

all_player_data = utils.get_all_player_data()

all_player_data = utils.transform_all_player_data(all_player_data)

price_points = utils.get_unique_price_points(all_player_data)

top_players = utils.get_top_players_per_price_point(all_player_data, price_points, 1 )

#create list of formations
#formations = [[5,4,1],[5,3,2],[4,4,2],[4,3,3],[3,5,2],[3,4,3]]
formations = [[3,5,2]]

#initiate club counter dictionary
clubs = {}
for i in range(1,21):
    clubs[i] = 0

#declare variables for using in nested loops below
budget = 100
bench_budgets = {}
bench_budgets['GK']  = 4.0
bench_budgets['DEF'] = 4.0
bench_budgets['MID'] = 4.5
bench_budgets['FWD'] = 4.5

results = {'Points': 0, 'Starting_XI': [], 'Cost': budget, 'Bench': []}
combinations_tested = 0

#loop through each combination of players
for formation in formations:
    bench_positions = {}
    bench_positions['GK'] = 1
    bench_positions['DEF'] = 5 - formation[0]
    bench_positions['MID'] = 5 - formation[1]
    bench_positions['FWD'] = 3 - formation[2]

    min_bench_budget = 0
    for position in bench_budgets:
        min_bench_budget += bench_budgets[position] * bench_positions[position]

    #And budget for starting XI
    starting_XI_budget = budget - min_bench_budget

    for gk in top_players['GK']:
        clubs[gk['club']] += 1
        for a in range(0,len(top_players['DEF']) - 2):
            clubs[top_players['DEF'][a]['club']] += 1
            for b in range(a+1,len(top_players['DEF']) - 1):
                clubs[top_players['DEF'][b]['club']] += 1
                for c in range(b+1,len(top_players['DEF'])):
                    if clubs[top_players['DEF'][c]['club']] == 3:
                        continue
                    else:
                        clubs[top_players['DEF'][c]['club']] += 1 
                    for d in range(0,len(top_players['MID']) - 4):
                        if clubs[top_players['MID'][d]['club']] == 3: 
                            continue
                        else:
                            clubs[top_players['MID'][d]['club']] += 1
                        for e in range(d + 1, len(top_players['MID']) - 3):
                            if clubs[top_players['MID'][e]['club']] == 3:
                                continue
                            else:
                                clubs[top_players['MID'][e]['club']] += 1
                            for f in range(e + 1, len(top_players['MID']) - 2):
                                if clubs[top_players['MID'][f]['club']] == 3:
                                    continue
                                else:
                                    clubs[top_players['MID'][f]['club']] += 1
                                for g in range(f + 1, len(top_players['MID']) - 1):
                                    if clubs[top_players['MID'][g]['club']] == 3:
                                        continue
                                    else:
                                        clubs[top_players['MID'][g]['club']] += 1
                                    for h in range(g + 1, len(top_players['MID'])):
                                        if clubs[top_players['MID'][h]['club']] == 3:
                                            continue
                                        else:
                                            clubs[top_players['MID'][h]['club']] += 1
                                        for i in range(0, len(top_players['FWD']) - 1):
                                            if clubs[top_players['FWD'][i]['club']] == 3: 
                                                continue
                                            else:
                                                clubs[top_players['FWD'][i]['club']] += 1
                                            for j in range(i + 1, len(top_players['FWD'])):
                                                if clubs[top_players['FWD'][j]['club']] == 3: 
                                                    continue
                                                else:
                                                    clubs[top_players['FWD'][j]['club']] += 1
                                                combinations_tested += 1

                                                #check if total points of XI higher than default/current toal
                                                points = gk['points'] + top_players['DEF'][a]['points'] + top_players['DEF'][b]['points'] + top_players['DEF'][c]['points'] + top_players['MID'][d]['points'] + top_players['MID'][e]['points'] + top_players['MID'][f]['points'] + top_players['MID'][g]['points'] + top_players['MID'][h]['points'] + top_players['FWD'][i]['points'] + top_players['FWD'][j]['points']
                                                if points >= results['Points']:
                                                    #now check cost - if wanted to return both teams that have equal pionts and price. could have elif: append
                                                    cost = gk['cost'] + top_players['DEF'][a]['cost'] + top_players['DEF'][b]['cost'] + top_players['DEF'][c]['cost'] + top_players['MID'][d]['cost'] + top_players['MID'][e]['cost'] + top_players['MID'][f]['cost'] + top_players['MID'][g]['cost'] + top_players['MID'][h]['cost'] + top_players['FWD'][i]['cost'] + top_players['FWD'][j]['cost']
                                                    if cost <= starting_XI_budget:
                                                        #get player names and add all data to results{}
                                                        starting_XI = [gk['name'], top_players['DEF'][a]['name'], top_players['DEF'][b]['name'], top_players['DEF'][c]['name'], top_players['MID'][d]['name'], top_players['MID'][e]['name'], top_players['MID'][f]['name'], top_players['MID'][g]['name'], top_players['MID'][h]['name'], top_players['FWD'][i]['name'], top_players['FWD'][j]['name']]
                                                        results['Starting_XI'] = starting_XI
                                                        results['Points'] = points
                                                        results['Cost'] = cost
                                                        results['Combination'] = combinations_tested
                                                        results['Clubs'] = clubs.copy()
                                                        pprint(results)
                                                        print('Combinations tested: ' + str(combinations_tested))
                                                        print(datetime.now())
                                                clubs[top_players['FWD'][j]['club']] -= 1
                                            clubs[top_players['FWD'][i]['club']] -= 1
                                        clubs[top_players['MID'][h]['club']] -= 1
                                    clubs[top_players['MID'][g]['club']] -= 1
                                clubs[top_players['MID'][f]['club']] -= 1
                            clubs[top_players['MID'][e]['club']] -= 1
                        clubs[top_players['MID'][d]['club']] -= 1
                    clubs[top_players['DEF'][c]['club']] -= 1
                clubs[top_players['DEF'][b]['club']] -= 1
            clubs[top_players['DEF'][a]['club']] -= 1
        clubs[gk['club']] -= 1

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