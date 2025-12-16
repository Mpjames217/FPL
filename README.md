# FPL
The Python scripts in this repository aim to select the optimal Fantasy Premier League squad.

There are a number of rules restricting squad selection, which can be found on the FPL website: https://fantasy.premierleague.com/help

 **Check out the teams progress here:** [Mpjames217_Python](https://fantasy.premierleague.com/entry/1577384/event/16)

 |Season|Total points|Global Ranking|Global Percentile|
 |------|------------|--------------|-----------------|
 |2024/2025|2181|3127383|27%|
 |2025/2026|819|4646321|37%|
 
 _*last updated: 2025-12-16 00:50:34_

## Scripts

**GW1_team_selector.py**

This script choses a squad based on total points. Can be used either before GW1 for initial squad selection or during the season when playing the wildcard.

This comprises a 0-1 Knapsack problem which is computationally difficult to fully solve. The following solutions were implemented as a compromise between completeness and performance:

- The pool of players is narrowed down to the top 3 players at each price point for each position

- Dynamic programming is then used to efficiently find the best starting XI, finding the best combinations of players in each position and then the best combination of these candidates.



 **transfer_selector.py**

Will select the best transfer to make based on their form and adjusted for the FDR or their next match.

Calls the team selector function to ensure the transfer selected has maximum gain in total gameweek points for the new strongest XI

**team_selector.py**

 Will select the best starting XI from the players currently in a given squad considering all possible formations and based on their form and adjusted for the FDR or their next match. 

 Chooses team Captain and Vice Captain.

 Calculates a predicted points total for the gameweek.

