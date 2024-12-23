from pprint import pprint
from operator import itemgetter
import utils.select_players, utils.api, utils.transform

def team_selector(squad_players, fixture_difficulty_ratings):  

    squad_players_by_position = {1: [], 2: [], 3: [], 4: []}

    for player in squad_players:
                player = utils.transform.calculate_predicted_points(player, fixture_difficulty_ratings)
                squad_players_by_position[player['element_type']].append(player)

    for position in squad_players_by_position:
        squad_players_by_position[position] = sorted(squad_players_by_position[position], key=itemgetter('predicted_points'), reverse=True)
   
    line_up = utils.select_players.get_line_up(squad_players_by_position)
    
    #select captain and vice captain
    squad_players = sorted(squad_players, key=itemgetter('predicted_points'), reverse=True)
    captain = squad_players[0]
    vice_captain = squad_players[1]

    line_up['total_predicted_points'] += captain['predicted_points']
    line_up['total_predicted_points'] = round(line_up['total_predicted_points'])
    line_up['Captain'] = captain['web_name']
    line_up['Vice Captain'] = vice_captain['web_name']

    return line_up

if __name__ == "__main__":
    response = utils.api.get_data('https://fantasy.premierleague.com/api/bootstrap-static')

    all_players = response['elements']
    current_gw = utils.api.get_current_gw(response)

    #team specific API call - gets the players currently in squad and transfer budget
    team_id = '8035167'
    team_info_address = 'https://fantasy.premierleague.com/api/entry/' + team_id + '/event/' + current_gw + '/picks'
    team_info = utils.api.get_data(team_info_address)

    fixture_difficulty_ratings, _ = utils.api.get_FDR_by_club(all_players)

    #get full information on players in the squad - team info only contains player IDs
    squad_players = []
    for player in all_players:
        for squad_player in team_info['picks']:
            if player['id'] == squad_player['element']:
                squad_players.append(player)

    pprint(team_selector(squad_players, fixture_difficulty_ratings))

