# FPL
The Python scripts in this repository aim to select the optimal Fantasy Premier League squad.

There are a number of rules restricting squad selection, which can be found on the FPL website: https://fantasy.premierleague.com/help

 **Check out the teams progress here:** [Mpjames217_Python](https://fantasy.premierleague.com/entry/8035167/event/22)

**GW1_team_selector.py**

This script choses a Gameweek 1 squad based on last seasons points totals and this seasons prices.

This comprises a 0-1 Knapsack problem which is computationally difficult to fully solve

V1.0 of this script, used for GW1 of the 24/25 season had the following limitations:

    - Use of reccursion over dynamic programming

    - Formation hard-coded as 3-5-2

    - Bench player selection limited to players from lowest price point

**team_selector.py**

 Will select the best starting XI from the players currently in a given squad considering all possible formations and based on their form and adjusted for the FDR or their next match. 

 Chooses team Captain and Vice Captain.

 Calculates a predicted points total for the gameweek.

**team_selector_function.py**

modified version of the team_selector script with the function modified to be callable as a util function

 **transfer_selector.py**

Will select the best transfer to make based on their form and adjusted for the FDR or their next match.

Calls the team selector function to ensure the transfer selected has maximum gain in total gameweek points for the new strongest XI
