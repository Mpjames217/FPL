import requests, json
from pprint import pprint
from datetime import datetime

#pull player data down from API
r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static').json()

#create and populate dictionary
#position is 'element_type' with 1 = GK, 2 = DF etc. May actually be much easier to leave like this to loop through!!!
players_API = {'GK': [], 'DEF': [], 'MID': [], 'FWD': []}
for player in r['elements']:
    #if player['web_name'] == 'Branthwaite':
        #pprint(player)
    if player['element_type'] == 1:
        position = 'GK'
    elif player['element_type'] == 2:
        position = 'DEF'
    elif player['element_type'] == 3:
        position = 'MID'
    elif player['element_type'] == 4:
        position = 'FWD'
    if player['chance_of_playing_next_round'] != 0:
        players_API[position].append({'name': player['web_name'], 'club': player['team'], 'cost': player['now_cost'] / 10, 'points': player['total_points']})

#get list of unique price pionts for each position
price_points = {}
for position in players_API:
    price_points[position] = []
    for player in players_API[position]:
        if player['cost'] not in price_points[position]:
            price_points[position].append(player['cost'])

#sort price points highest to lowest
for position in price_points:
    price_points[position].sort(reverse=True)

#get top players for each price point in each position
top_players = {}
players_per_price_point = 2

#for each price point
for position in price_points:
    top_players[position] = {}
    for price_point in price_points[position]:
        top_players[position][price_point] = []
        #for each player in position, add to top players if higher points than players already there, or less than max in each position
        for player in players_API[position]:
            if player['cost'] == price_point and player['points'] > 99:
                if len(top_players[position][price_point]) < players_per_price_point:
                    top_players[position][price_point].append(player)
                #loop through players already in top players and replace if current player pionts are higher
                else:
                    for i in range(len(top_players[position][price_point])):
                        if player['points'] > top_players[position][price_point][i]['points']:
                            top_players[position][price_point][i] = player
                            break

#Populate players{} without the price point keys
players = {}
for position in top_players:
    players[position] = []
    for price_point in top_players[position]:
        for player in top_players[position][price_point]:
            players[position].append(player)

#pprint(players)

#create list of formations
#formations = [[5,4,1],[5,3,2],[4,4,2],[4,3,3],[3,5,2],[3,4,3]]
#scaled down to one formation for intial development
formations = [[3,5,2]]

#For each formation, calculate minimum budget needed for the bench.
budget = 100
bench_budgets = {}
bench_budgets['GK']  = 4.0
bench_budgets['DEF'] = 4.0
bench_budgets['MID'] = 4.5
bench_budgets['FWD'] = 4.5

bench_positions = {}
bench_positions['GK'] = 1
bench_positions['DEF'] = 5 - formations[0][0]
bench_positions['MID'] = 5 - formations[0][1]
bench_positions['FWD'] = 3 - formations[0][2]

min_bench_budget = 0
for position in bench_budgets:
    min_bench_budget += bench_budgets[position] * bench_positions[position]

#And budget for starting XI
starting_XI_budget = budget - min_bench_budget

#initiate club counter dictionary
clubs = {}
for i in range(1,21):
    clubs[i] = 0

#declare variables for using in nested loops below
results = {'Points': 0, 'Starting_XI': '', 'Cost': starting_XI_budget, 'Bench': []}
combinations_tested = 0

#could have if player cost == same postion in startingXI and points <, continue ?


#loop through each combination of players
for gk in players['GK']: #for each GK
    clubs[gk['club']] += 1
    for a in range(0,len(players['DEF']) - 2):
        clubs[players['DEF'][a]['club']] += 1
        for b in range(a+1,len(players['DEF']) - 1):
            clubs[players['DEF'][b]['club']] += 1
            for c in range(b+1,len(players['DEF'])):
                if clubs[players['DEF'][c]['club']] == 3:
                    continue
                else:
                   clubs[players['DEF'][c]['club']] += 1 
                for d in range(0,len(players['MID']) - 4):
                    if clubs[players['MID'][d]['club']] == 3: 
                        continue
                    else:
                        clubs[players['MID'][d]['club']] += 1
                    for e in range(d + 1, len(players['MID']) - 3):
                        if clubs[players['MID'][e]['club']] == 3:
                            continue
                        else:
                            clubs[players['MID'][e]['club']] += 1
                        for f in range(e + 1, len(players['MID']) - 2):
                            if clubs[players['MID'][f]['club']] == 3:
                                continue
                            else:
                                clubs[players['MID'][f]['club']] += 1
                            for g in range(f + 1, len(players['MID']) - 1):
                                if clubs[players['MID'][g]['club']] == 3:
                                    continue
                                else:
                                    clubs[players['MID'][g]['club']] += 1
                                for h in range(g + 1, len(players['MID'])):
                                    if clubs[players['MID'][h]['club']] == 3:
                                        continue
                                    else:
                                        clubs[players['MID'][h]['club']] += 1
                                    for i in range(0, len(players['FWD']) - 1):
                                        if clubs[players['FWD'][i]['club']] == 3: 
                                            continue
                                        else:
                                            clubs[players['FWD'][i]['club']] += 1
                                        for j in range(i + 1, len(players['FWD'])):
                                            if clubs[players['FWD'][j]['club']] == 3: 
                                                continue
                                            else:
                                                clubs[players['FWD'][j]['club']] += 1
                                            combinations_tested += 1

                                            #check if total points of XI higher than default/current toal
                                            points = gk['points'] + players['DEF'][a]['points'] + players['DEF'][b]['points'] + players['DEF'][c]['points'] + players['MID'][d]['points'] + players['MID'][e]['points'] + players['MID'][f]['points'] + players['MID'][g]['points'] + players['MID'][h]['points'] + players['FWD'][i]['points'] + players['FWD'][j]['points']
                                            if points >= results['Points']:
                                                #now check cost - if wanted to return both teams that have equal pionts and price. could have elif: append
                                                cost = gk['cost'] + players['DEF'][a]['cost'] + players['DEF'][b]['cost'] + players['DEF'][c]['cost'] + players['MID'][d]['cost'] + players['MID'][e]['cost'] + players['MID'][f]['cost'] + players['MID'][g]['cost'] + players['MID'][h]['cost'] + players['FWD'][i]['cost'] + players['FWD'][j]['cost']
                                                if cost <= starting_XI_budget:
                                                    #get player names and add all data to results{}
                                                    starting_XI = [gk['name'], players['DEF'][a]['name'], players['DEF'][b]['name'], players['DEF'][c]['name'], players['MID'][d]['name'], players['MID'][e]['name'], players['MID'][f]['name'], players['MID'][g]['name'], players['MID'][h]['name'], players['FWD'][i]['name'], players['FWD'][j]['name']]
                                                    results['Starting_XI'] = starting_XI
                                                    results['Points'] = points
                                                    results['Cost'] = cost
                                                    results['Combination'] = combinations_tested
                                                    results['Clubs'] = clubs.copy()
                                                    #pprint(results)
                                                    #print('Combinations tested: ' + str(combinations_tested))
                                                    #print(datetime.now())
                                            clubs[players['FWD'][j]['club']] -= 1
                                        clubs[players['FWD'][i]['club']] -= 1
                                    clubs[players['MID'][h]['club']] -= 1
                                clubs[players['MID'][g]['club']] -= 1
                            clubs[players['MID'][f]['club']] -= 1
                        clubs[players['MID'][e]['club']] -= 1
                    clubs[players['MID'][d]['club']] -= 1
                clubs[players['DEF'][c]['club']] -= 1
            clubs[players['DEF'][b]['club']] -= 1
        clubs[players['DEF'][a]['club']] -= 1
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
        for player in players_API[position]:
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

del results['Clubs']
pprint(results)