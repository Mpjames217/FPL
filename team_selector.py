import requests, json
from pprint import pprint
from datetime import datetime

#pull player data down from API
r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static').json()
players_API = r['elements']

#create and populate dictionary
#position is 'element_type' with 1 = GK, 2 = DF etc. May actually be much easier to leave like this to loop through!!!
players = {'GK': [], 'DEF': [], 'MID': [], 'FWD': []}
for player in players_API:
    if player['element_type'] == 1:
        position = 'GK'
    elif player['element_type'] == 2:
        position = 'DEF'
    elif player['element_type'] == 3:
        position = 'MID'
    elif player['element_type'] == 4:
        position = 'FWD'
    players[position].append({'name': player['web_name'], 'club': player['team'], 'cost': player['now_cost'] / 10, 'points': player['total_points']})

#get list of unique price pionts for each position
price_points = {}
for position in players:
    price_points[position] = []
    for player in players[position]:
        if player['cost'] not in price_points[position]:
            price_points[position].append(player['cost'])

#sort price points highest to lowest
for position in price_points:
    price_points[position].sort(reverse=True)

#get top 5 players for each price piont in each position
top_players = {}

#for each price point
for position in price_points:
    top_players[position] = {}
    for price_point in price_points[position]:
        top_players[position][price_point] = []
        #for each player in position, add to top players if higher points than players already there, or less than 5 in each position
        for player in players[position]:
            if player['cost'] == price_point:
                if len(top_players[position][price_point]) < 2:
                    top_players[position][price_point].append(player)
                #loop through players already in top players and replace if current player pionts are higher
                else:
                    for i in range(len(top_players[position][price_point])):
                        if player['points'] > top_players[position][price_point][i]['points']:
                            top_players[position][price_point][i] = player
                            break

#repopulate players[] without the price point keys
players = {}
for position in top_players:
    players[position] = []
    for price_point in top_players[position]:
        for player in top_players[position][price_point]:
            players[position].append(player)

pprint(players)

#create list of formations
#formations = [[5,4,1],[5,3,2],[4,4,2],[4,3,3],[3,5,2],[3,4,3]]
#scaled down to one formation for intial development
formations = [[3,5,2]]

#For each formation, calculate minimum budget needed for the bench.
squad_price = 0
budget = 100
min_GK_price = 4.0
min_DF_price = 4.0
min_MD_price = 4.5
min_FD_price = 4.5

bench_GK = 1
bench_DF = 5 - formations[0][0]
bench_MD = 5 - formations[0][1]
bench_FD = 3 - formations[0][2]

min_bench_budget = bench_GK * min_GK_price + bench_DF * min_DF_price + bench_MD * min_MD_price + bench_FD * min_FD_price

#And budget for starting XI
starting_XI_budget = budget - min_bench_budget

#declare variables for using in nested loops below
results = {'Points': 0, 'Starting_XI': '', 'Cost': starting_XI_budget}
combinations_tested = 0

#initiate club counter dictionary
clubs = {}
for i in range(1,21):
    clubs[i] = 0

#could have if player cost == same postion in startingXI and points <, continue ?


#loop through each combination of players
for gk in players['GK']: #for each GK
    clubs[gk['club']] += 1
    print(gk)
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
                                            if clubs[players['FWD'][j]['club']] > 3: 
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
                                                    #add check here for clubs played for

                                                    #get player names and add all data to results{}
                                                    starting_XI = [gk['name'], players['DEF'][a]['name'], players['DEF'][b]['name'], players['DEF'][c]['name'], players['MID'][d]['name'], players['MID'][e]['name'], players['MID'][f]['name'], players['MID'][g]['name'], players['MID'][h]['name'], players['FWD'][i]['name'], players['FWD'][j]['name']]
                                                    results['Starting_XI'] = starting_XI
                                                    results['Points'] = points
                                                    results['Cost'] = cost
                                                    results['Combination'] = combinations_tested
                                                    pprint(results)
                                                    print('Combinations tested: ' + str(combinations_tested))
                                                    print(datetime.now())
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

pprint(results)
print('FINAL Combinations tested: ' + str(combinations_tested))

#fill bench - select best players at lowest price piont for each empty position where player per team limit is not exceeded
#determine bench order - order by average predicted pionts/value or by enforced substitutions?

#find best player for position one

#repeat for positions 2-3