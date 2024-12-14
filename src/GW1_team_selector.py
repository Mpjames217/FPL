from pprint import pprint
import utils
import select_players_utils

def main():
    all_player_data = utils.get_all_player_data()
    all_player_data = utils.transform_all_player_data(all_player_data)

    #experiemnt without these just using all player data
    price_points = utils.get_unique_price_points(all_player_data)
    top_players = utils.get_top_players_per_price_point(all_player_data, price_points, 1 )

    #formations = [[5,4,1],[5,3,2],[4,4,2],[4,3,3],[3,5,2],[3,4,3]]
    formations = [[3,5,2]]
    budget = 100

    results = {'formation': [], 'Starting_XI': {'Points': 0}, 'Bench_players': []}

    for formation in formations:
        def_slots = formation[0]
        mid_slots = formation[1]
        fwd_slots = formation[2]

        bench_positions = {}
        bench_positions['GK'] = 1
        bench_positions['DEF'] = 5 - def_slots
        bench_positions['MID'] = 5 - mid_slots
        bench_positions['FWD'] = 3 - fwd_slots

        min_bench_budget = utils.get_min_bench_budget(bench_positions)
        starting_XI_budget = budget - min_bench_budget

        n_combinations = 50

        top_GKs = select_players_utils.get_top_player_combinations(top_players['GK'], 1, n_combinations)
        top_defences = select_players_utils.get_top_player_combinations(top_players['DEF'], def_slots, n_combinations)
        top_midfields = select_players_utils.get_top_player_combinations(top_players['MID'], mid_slots, n_combinations)
        top_forwards = select_players_utils.get_top_player_combinations(top_players['FWD'], fwd_slots, n_combinations)

        starting_xi = select_players_utils.get_starting_xi(top_GKs, top_defences, top_midfields, top_forwards, starting_XI_budget)

        if starting_xi['points'] > results['Starting_XI']['Points']:
            results['formation'] = formation
            results['Starting_XI'] = starting_xi

            bench_budget = budget - starting_xi['cost']
            results['Bench_players'] = select_players_utils.get_bench_players(bench_positions, all_player_data)

    pprint(results)

if __name__ == "__main__":
    main()