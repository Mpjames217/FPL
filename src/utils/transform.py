from operator import itemgetter

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

def calculate_predicted_points(player, fixture_difficulty_ratings, mode='average'):
    
    FDR = fixture_difficulty_ratings[player['team']]
    predicted_points = 0
    player['form'] = float(player['form'])

    if mode == 'average':
        for gw in FDR.values():
            for fixture in gw:
                modified_FDR = 1 + ((fixture - 2) /10)
                predicted_points += player['form'] * modified_FDR
        predicted_points /= 3

    if mode == 'next_match':
        gw = list(FDR.values())[0]
        for fixture in gw:
            modified_FDR = 1 + ((fixture - 2) /10)
            predicted_points += player['form'] * modified_FDR
    
    if player['chance_of_playing_next_round'] != None:
        predicted_points *= (player['chance_of_playing_next_round']/ 100)

    player['predicted_points'] = predicted_points
    return player

def get_possible_transfers(form_players, squad_players, transfer_budget):
    '''Returns a list of possible transfers where predicted point delta exceeds 4'''
    possible_transfers = []

    for form_player in form_players:
        for squad_player in squad_players:
            if form_player['element_type'] == squad_player['element_type'] and form_player['predicted_points'] > squad_player['predicted_points'] + 4 and form_player['now_cost'] <= squad_player['now_cost'] + transfer_budget:
                #check max players per club not exceeded
                # if clubs[form_player['team']]['count'] < 3 or form_player['team'] == squad_player['team']:
                pp_delta = round(form_player['predicted_points'] - squad_player['predicted_points'], 2)
                possible_transfers.append({'player_in': form_player['web_name'], 'player_out': squad_player['web_name'], 'pp_delta': pp_delta})


    #order transfers by point_delta
    return sorted(possible_transfers, key=itemgetter('pp_delta'), reverse=True)
