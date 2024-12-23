from pprint import pprint
import team_selector
import utils.select_players, utils.api, utils.transform

def transfer_suggester():

    response = utils.api.get_data('https://fantasy.premierleague.com/api/bootstrap-static')

    all_players = response['elements']
    current_gw = utils.api.get_current_gw(response)

    #team specific API call - gets the players currently in squad and transfer budget
    team_id = '8035167'
    team_info_address = 'https://fantasy.premierleague.com/api/entry/' + team_id + '/event/' + current_gw + '/picks'

    team_info = utils.api.get_data(team_info_address)
    transfer_budget = team_info['entry_history']['bank']

    FDR_next_match, FDR_average = utils.api.get_FDR_by_club(all_players)

    #get full information on players in the squad and compile list of form players for each position - team info only contains player IDs
    squad_players = []
    form_players = []

    for player in all_players:
        player = utils.transform.calculate_predicted_points(player, FDR_average)
        
        for squad_player in team_info['picks']:
            if player['id'] == squad_player['element']:
                squad_players.append(player)

        if player['form_rank_type'] < 10 and player not in squad_players and player['chance_of_playing_next_round'] != 0:
            form_players.append(player)

    possible_transfers = utils.transform.get_possible_transfers(form_players, squad_players, transfer_budget)
    if not possible_transfers:
        print('No transfer reccomended')
        current_gw_squad = squad_players
    else:
        line_ups = utils.transform.sort_transfers_by_first_xi_impact(possible_transfers, squad_players, form_players, FDR_average)
        print(line_ups[0]['transfer'])
        current_gw_squad = line_ups[0]['squad']

    current_gw_line_up = team_selector.team_selector(current_gw_squad, FDR_next_match)
    current_gw_line_up['total_predicted_points'] = round(current_gw_line_up['total_predicted_points'])

    pprint(current_gw_line_up)

if __name__ == "__main__":
    transfer_suggester()
