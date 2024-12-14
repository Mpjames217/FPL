import requests

def get_all_player_data():
    try:
        result = requests.get('https://fantasy.premierleague.com/api/bootstrap-static').json()
        return result['elements']
    
    except:
        print('Error encounted accessing API. Execution will terminate')
        exit()
    

def transform_all_player_data(all_player_data):
    refactored_data = {'GK': [], 'DEF': [], 'MID': [], 'FWD': []}
    for player in all_player_data:
        if player['element_type'] == 1:
            position = 'GK'
        elif player['element_type'] == 2:
            position = 'DEF'
        elif player['element_type'] == 3:
            position = 'MID'
        elif player['element_type'] == 4:
            position = 'FWD'
        if player['chance_of_playing_next_round'] != 0:
            refactored_data[position].append({'name': player['web_name'], 'club': player['team'], 'cost': player['now_cost'] / 10, 'points': player['total_points']})
    
    return refactored_data

def get_unique_price_points(all_players_data):
    price_points = {}
    for position in all_players_data:
        price_points[position] = []
        for player in all_players_data[position]:
            if player['cost'] not in price_points[position]:
                price_points[position].append(player['cost'])

    for position in price_points:
        price_points[position].sort(reverse=True)

    return price_points

def get_top_players_per_price_point(all_player_data, price_points, players_per_price_point):
    top_players = {}

    #for each price point
    for position in price_points:
        top_players[position] = {}
        for price_point in price_points[position]:
            top_players[position][price_point] = []
            #for each player in position, add to top players if higher points than players already there, or less than max in each position
            for player in all_player_data[position]:
                if player['cost'] == price_point and player['points'] > 42:
                    if len(top_players[position][price_point]) < players_per_price_point:
                        top_players[position][price_point].append(player)
                    #loop through players already in top players and replace if current player points are higher
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

    return players

def get_min_bench_budget(bench_positions):

    bench_budgets = {}
    # hard coded values to be replaced with a function that finds the cheapest players for a given position
    bench_budgets['GK']  = 4.0
    bench_budgets['DEF'] = 4.0
    bench_budgets['MID'] = 4.5
    bench_budgets['FWD'] = 4.5

    min_bench_budget = 0
    for position in bench_budgets:
        min_bench_budget += bench_budgets[position] * bench_positions[position]

    return min_bench_budget

