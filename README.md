# FPL
The Python scripts in this repository aim to select the optimal Fantasy Premier League squad.

There are a number of rules restricting squad selection, which can be found on the FPL website: https://fantasy.premierleague.com/help

The team chosen and modified based on these scripts has been entered as Mpjames217_Python

team_selector.py
This script choses a Gameweek 1 squad based on last seasons points totals and this seasons prices.

This comprises a 0-1 Knapsack problem which is computationally difficult to fully solve

V1.0 of this script, used for GW1 of the 24/25 season has the following limitations:
    - Use of reccursion over dynamic programming
    - Formation hard-coded as 3-5-2
    - Bench player selection limited to players from lowest price point
