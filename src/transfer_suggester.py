import os
import asyncio
from dotenv import load_dotenv
from pprint import pprint
from src.team_selector import team_selector
from src.utils.sort_by_first_xi import sort_transfers_by_first_xi_impact
import src.utils.api as api
import src.utils.transform as transform

def transfer_suggester():

    response = api.get_data('https://fantasy.premierleague.com/api/bootstrap-static')

    all_players = response['elements']
    current_gw = api.get_current_gw(response)

    #team specific API call - gets the players currently in squad and transfer budget
    load_dotenv(override=True)
    team_id = os.environ.get("team_id")
    team_info_address = 'https://fantasy.premierleague.com/api/entry/' + team_id + '/event/' + current_gw + '/picks'

    team_info = api.get_data(team_info_address)
    transfer_budget = team_info['entry_history']['bank']

    upcoming_FDR = asyncio.run(api.get_FDR_by_club(all_players, current_gw))

    #get full information on players in the squad and compile list of form players for each position - team info only contains player IDs
    squad_players = []
    form_players = []
    clubs = {club: 0 for club in range(1,21)}

    for player in all_players:
        player = transform.calculate_predicted_points(player, upcoming_FDR)
        
        for squad_player in team_info['picks']:
            if player['id'] == squad_player['element']:
                squad_players.append(player)
                clubs[player['team']] += 1

        if player['form_rank_type'] < 10 and player not in squad_players and player['chance_of_playing_next_round'] != 0:
            form_players.append(player)

    possible_transfers = transform.get_possible_transfers(form_players, squad_players, transfer_budget, clubs)
    
    if not possible_transfers:
        print('No transfer reccomended')
        current_gw_squad = squad_players
    else:
        line_ups = sort_transfers_by_first_xi_impact(possible_transfers, squad_players, form_players)
        print(line_ups[0]['transfer'])
        current_gw_squad = line_ups[0]['squad']

    for player in current_gw_squad:
        player = transform.calculate_predicted_points(player, upcoming_FDR, mode='next_match')

    current_gw_line_up = team_selector(current_gw_squad)
    current_gw_line_up['total_predicted_points'] = round(current_gw_line_up['total_predicted_points'])

    pprint(current_gw_line_up)

if __name__ == "__main__":
    transfer_suggester()
