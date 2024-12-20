from pprint import pprint
import team_selector
import utils.select_players, utils.api, utils.transform

#make calculate predicted points into function?
#Next steps: take into acount Double Gameweeks (DGWs), consider more than one transfer, combine with team_selector to factor in increase in first XI points?
#Maybe do one transfer by biggest form gain and only do multiple if improves first XI total points?

response = utils.api.get_data('https://fantasy.premierleague.com/api/bootstrap-static')

all_players = response['elements']
current_gw = utils.api.get_current_gw(response)

#team specific API call
team_id = '8035167'
team_info_address = 'https://fantasy.premierleague.com/api/entry/' + team_id + '/event/' + current_gw + '/picks'
team_info = utils.api.get_data(team_info_address)
transfer_budget = team_info['entry_history']['bank']

fixture_difficulty_ratings = utils.api.get_FDR_by_club(all_players)

#get full information on players in the squad and compile list of form players for each position

squad_players = []
form_players = []

for player in all_players:
    player = utils.transform.calculate_predicted_points(player, fixture_difficulty_ratings)
    
    for squad_player in team_info['picks']:
        if player['id'] == squad_player['element']:
            squad_players.append(player)

    if player['form_rank_type'] < 10 and player not in squad_players and player['chance_of_playing_next_round'] != 0:
        form_players.append(player)

#make a list of possible transfers where predicted point delta exceeds 2
possible_transfers = utils.transform.get_possible_transfers(form_players, squad_players, transfer_budget)

#inspect up to the top 10 transfers
line_ups = utils.transform.sort_transfers_by_first_xi_impact(possible_transfers, squad_players, form_players, fixture_difficulty_ratings)

if line_ups:
    print(line_ups[0]['transfer'])
    current_gw_squad = line_ups[0]['squad']
    
else:
    print('No transfer reccomended')
    current_gw_squad = squad_players

current_gw_line_up = team_selector.team_selector(current_gw_squad, fixture_difficulty_ratings, 'next_match_FDR')
current_gw_line_up['total_predicted_points'] = round(current_gw_line_up['total_predicted_points'])

pprint(current_gw_line_up)
