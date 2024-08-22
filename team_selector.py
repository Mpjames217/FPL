import requests
from pprint import pprint
import math

r = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/').json()
players_API = r['elements']

players = {'GK': [], 'DEF': [], 'MID': [], 'FWD': []}
positionCosts = {'GK': [], 'DEF': [], 'MID': [], 'FWD': []}
for player in players_API:
    if player['element_type'] == 1:
        position = 'GK'
    elif player['element_type'] == 2:
        position = 'DEF'
    elif player['element_type'] == 3:
        position = 'MID'
    elif player['element_type'] == 4:
        position = 'FWD'

    players[position].append({
        'name': player['web_name'],
        'club': player['team'],
        'cost': player['now_cost'] / 10,
        'points': player['total_points'],
        'id': player['id']
    })
    positionCosts[position].append(player['now_cost'] / 10)

formations = [
	[1, 3, 5, 2],
	[1, 3, 4, 3],
	[1, 4, 4, 2],
	[1, 4, 3, 3],
	[1, 4, 5, 1],
	[1, 5, 3, 2],
	[1, 5, 4, 1],
	[1, 5, 2, 3],
]

for formation in formations:
	pprint(formation)
	minBenchCost = min(positionCosts['GK']) + ((5 - formation[1]) * min(positionCosts['DEF'])) + ((5 - formation[2]) *  min(positionCosts['MID'])) + ((3 - formation[3]) *  min(positionCosts['FWD']))

	budget = 100 - minBenchCost  # Set the total budget to 100 units

	# Construct a list of players for each position in the formation
	positions = [[]]
	for x in range (formation[0]):
		positions.append(players['GK'])
	for x in range (formation[1]):
	    positions.append(players['DEF'])
	for x in range (formation[2]):
	    positions.append(players['MID'])
	for x in range (formation[3]):
	    positions.append(players['FWD'])

	# DP table to store maximum points for each position and budget
	dp = [[{'points': -float('inf'), 'used': set(), 'player': None, 'team_count': {}}
		  for _ in range(int(budget * 10) + 1)] for _ in range(12)]  # Initialize the DP table with negative infinity points

	dp[0][0] = {'points': 0, 'used': set(), 'player': None, 'team_count': {}}  # Base case: no players, zero cost, zero points

	# Populate the DP table
	for pos in range(1, 12):  # Loop through each position in the starting XI (1 to 11)
		for player in positions[pos]:  # Loop through each player eligible for the current position
			player_cost = int(player["cost"] * 10)
			player_points = player["points"]
			player_team = player['club']

			for b in range(int(budget * 10), player_cost - 1, -1):  # Loop through possible budgets from high to low
				if dp[pos - 1][b - player_cost]['points'] != -float('inf'):  # Check if the previous state is valid
					new_points = dp[pos - 1][b - player_cost]['points'] + player_points  # Calculate new total points
					new_team_count = dp[pos - 1][b - player_cost]['team_count'].copy()  # Copy the team count dictionary

					# Initialize the team count if this team hasn't been used yet
					if player_team not in new_team_count:
						new_team_count[player_team] = 0
					new_team_count[player_team] += 1  # Increment the count for the player's team

					# Ensure no more than 3 players from the same team are selected and update the DP table if better
					if (new_team_count[player_team] <= 3 and
						new_points > dp[pos][b]['points'] and
						player['id'] not in dp[pos - 1][b - player_cost]['used']):
						dp[pos][b] = {
							'points': new_points,  # Update the points in the DP table
							'used': dp[pos - 1][b - player_cost]['used'].union({player['id']}),  # Track used players
							'player': player['id'],  # Track the current player
							'team_count': new_team_count  # Update the team count
						}

	# Traceback to determine the selected players
	best_team = []

	# Find the budget that gives the maximum points for the last position
	b = max(range(int(budget * 10) + 1), key=lambda x: dp[11][x]['points'])
	for pos in range(11, 0, -1):  # Backtrack from the last position to the first
		if dp[pos][b]['points'] != -float('inf'):  # Ensure the state is valid
			player_idx = dp[pos][b]['player']  # Get the player index from the DP table
			if player_idx is not None:
				for player in positions[pos]:
					if (player["id"] == player_idx):
						best_team.append(player)  # Add the player to the best team list
						b -= int(player["cost"] * 10)  # Subtract the player's cost from the remaining budget

	best_team.reverse()
	max_points = dp[11][max(range(int(budget * 10) + 1), key=lambda x: dp[11][x]['points'])]['points']

	pprint("rating: " + str(max_points))
	pprint("cost: " + str(max(range(int(budget * 10) + 1), key=lambda x: dp[11][x]['points']) / 10))
	pprint(best_team)

	#This doesn't work well with the multiple formations
	"""bestBench = {'GK': {'points': 0}, 'DEF': {'points': 0}, 'FWD': {'points': 0}}
	for pos in bestBench.keys():
		for player in players[pos]:
			if min(positionCosts[pos]) == player['cost'] and player['points'] > bestBench[pos]['points']:
				bestBench[pos] = player

	pprint(bestBench)"""