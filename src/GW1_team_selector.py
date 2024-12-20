from pprint import pprint
import utils.select_players, utils.api, utils.transform

def main():
    all_player_data = utils.api.get_data('https://fantasy.premierleague.com/api/bootstrap-static')['elements']
    all_player_data = utils.transform.transform_all_player_data(all_player_data)

    price_points = utils.transform.get_unique_price_points(all_player_data)
    top_players = utils.select_players.get_top_players_per_price_point(all_player_data, price_points, 3 )

    formations = [[5,4,1],[5,3,2],[4,4,2],[4,3,3],[3,5,2],[3,4,3]]
    budget = 100

    results = {'formation': [], 'Starting_XI': {'points': 0}, 'Bench_players': []}

    for formation in formations:
        def_slots = formation[0]
        mid_slots = formation[1]
        fwd_slots = formation[2]

        bench_positions = {}
        bench_positions['GK'] = 1
        bench_positions['DEF'] = 5 - def_slots
        bench_positions['MID'] = 5 - mid_slots
        bench_positions['FWD'] = 3 - fwd_slots

        min_bench_budget = utils.transform.get_min_bench_budget(bench_positions)
        starting_XI_budget = budget - min_bench_budget

        n_combinations = 20

        top_GKs = utils.select_players.get_top_player_combinations(top_players['GK'], 1, n_combinations)
        top_defences = utils.select_players.get_top_player_combinations(top_players['DEF'], def_slots, n_combinations)
        top_midfields = utils.select_players.get_top_player_combinations(top_players['MID'], mid_slots, n_combinations)
        top_forwards = utils.select_players.get_top_player_combinations(top_players['FWD'], fwd_slots, n_combinations)

        starting_xi = utils.select_players.get_starting_xi(top_GKs, top_defences, top_midfields, top_forwards, starting_XI_budget)

        if starting_xi['points'] > results['Starting_XI']['points']:
            results['formation'] = formation
            results['Starting_XI'] = starting_xi

            bench_budget = budget - starting_xi['cost']
            results['Bench_players'] = utils.select_players.get_bench_players(bench_positions, all_player_data)

    pprint(results)

if __name__ == "__main__":
    main()