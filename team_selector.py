#Python script to select GW1 squad - using maunally entered player data with estimated season pionts for now
from pprint import pprint

#simulated player data (expand to see):
players = {
    'GK' : [
    {
        'Name' : 'Pickford',
        'Club' : 'Everton',
        'Price': 5.0,
        'Points':150
    },
    {
        'Name' : 'Flekken',
        'Club' : 'Crystal Palace',
        'Price': 4.5,
        'Points':110
    },
    {
        'Name' : 'Fabianski',
        'Club' : 'West Ham',
        'Price': 4.0,
        'Points':30
    }
    ],
    'DEF' : [
    {
        'Name' : 'Saliba',
        'Club' : 'Arsenal',
        'Price': 6.0,
        'Points':160
    },
    {
        'Name' : 'White',
        'Club' : 'Arsenal',
        'Price':  6.5,
        'Points': 170
    },
        {
        'Name' : 'Gabriel',
        'Club' : 'Arsenal',
        'Price':  6.0,
        'Points': 150
    },
        {
        'Name' : 'Trent',
        'Club' : 'Liverpool',
        'Price':  7.0,
        'Points': 180
    },
        {
        'Name' : 'Pedro Porro',
        'Club' : 'Tottenham',
        'Price':  5.5,
        'Points': 130
    },
        {
        'Name' : 'Schar',
        'Club' : 'Newcastle',
        'Price':  5.5,
        'Points': 120
    },
        {
        'Name' : 'Andersen',
        'Club' : 'Crystal Palace',
        'Price':  5.5,
        'Points': 120
    },
        {
        'Name' : 'Dalot',
        'Club' : 'Manchester United',
        'Price':  5.0,
        'Points': 110
    },
        {
        'Name' : 'Tarkowski',
        'Club' : 'Everton',
        'Price':  5.0,
        'Points': 100
    },
        {
        'Name' : 'Branthwaite',
        'Club' : 'Everton',
        'Price':  5.0,
        'Points': 100
    },
        {
        'Name' : 'Burn',
        'Club' : 'Newcastle',
        'Price':  4.5,
        'Points': 100
    },
        {
        'Name' : 'Mykelenko',
        'Club' : 'Everton',
        'Price':  4.5,
        'Points': 100
    },
        {
        'Name' : 'Robinson',
        'Club' : 'Fulham',
        'Price':  4.5,
        'Points': 80
    },
        {
        'Name' : 'Johnson',
        'Club' : 'Ipswich',
        'Price':  4.0,
        'Points': 40
    },
        {
        'Name' : 'Harwood-Ellis',
        'Club' : 'Southampton',
        'Price':  4.0,
        'Points': 40
    },
    ],
    'MID': [
        {
        'Name' : 'Foden',
        'Club' : 'Manchester City',
        'Price': 9.5,
        'Points':180
    },
    {
        'Name' : 'Palmer',
        'Club' : 'Chelsea',
        'Price':  10.5,
        'Points': 180
    },
        {
        'Name' : 'Nkuku',
        'Club' : 'Chelsea',
        'Price':  6.5,
        'Points': 180
    },
        {
        'Name' : 'Amad',
        'Club' : 'Manchester United',
        'Price':  5.0,
        'Points': 100
    },
        {
        'Name' : 'Winks',
        'Club' : 'Ipswich',
        'Price': 4.5,
        'Points': 70
    },
    {
        'Name' : 'Salah',
        'Club' : 'Liverpool',
        'Price':  12.5,
        'Points': 230
    },
        {
        'Name' : 'Maddison',
        'Club' : 'Tottenham',
        'Price':  7.5,
        'Points': 150
    },
        {
        'Name' : 'Son',
        'Club' : 'Tottenham',
        'Price':  10.0,
        'Points': 150
    },
        {
        'Name' : 'Elanga',
        'Club' : 'Nottingham Forrest',
        'Price': 5.5,
        'Points':125
    },
    {
        'Name' : 'Hudson-Odoi',
        'Club' : 'Nottingham Forrest',
        'Price':  5.5,
        'Points': 110
    },
        {
        'Name' : 'Morgan Gibbs-White',
        'Club' : 'Nottingham Forrest',
        'Price':  6.5,
        'Points': 140
    },
        {
        'Name' : 'Gordon',
        'Club' : 'Newcastle',
        'Price':  7.5,
        'Points': 170
    },
        {
        'Name' : 'Odegaard',
        'Club' : 'Arsenal',
        'Price':  8.5,
        'Points': 180
    },
        {
        'Name' : 'Saka',
        'Club' : 'Arsenal',
        'Price':  10.0,
        'Points': 180
    },
        {
        'Name' : 'Kudas',
        'Club' : 'West Ham',
        'Price':  6.5,
        'Points': 130
    },
        {
        'Name' : 'Garnacho',
        'Club' : 'Manchester United',
        'Price':  6.5,
        'Points': 130
    },
        {
        'Name' : 'Andreas',
        'Club' : 'Fulham',
        'Price':  5.5,
        'Points': 120
    },
        {
        'Name' : 'Soucek',
        'Club' : 'West Ham',
        'Price':  5.0,
        'Points': 100
    },

        {
        'Name' : 'Ahamada',
        'Club' : 'Cystal Palace',
        'Price':  4.5,
        'Points': 70
    },
        {
        'Name' : 'Szoboszlai',
        'Club' : 'Liverpool',
        'Price':  6.5,
        'Points': 170
    }
    ],
    'FWD': [
            {
        'Name' : 'Haaland',
        'Club' : 'Manchester City',
        'Price': 15.0,
        'Points':300
    },
    {
        'Name' : 'Watkins',
        'Club' : 'Aston Villa',
        'Price':  9.0,
        'Points': 180
    },
        {
        'Name' : 'Havertz',
        'Club' : 'Arsenal',
        'Price':  8.0,
        'Points': 180
    },
        {
        'Name' : 'Isaak',
        'Club' : 'Newcastle',
        'Price':  8.5,
        'Points': 180
    },
        {
        'Name' : 'Cunha',
        'Club' : 'Wolves',
        'Price':  6.5,
        'Points': 130
    },
        {
        'Name' : 'Joao Pedro',
        'Club' : 'Brighton',
        'Price':  5.5,
        'Points': 100
    },
        {
        'Name' : 'Archer',
        'Club' : 'Aston Villa',
        'Price':  5.0,
        'Points': 80
    },
        {
        'Name' : 'Fraser',
        'Club' : 'Wolves',
        'Price':  4.5,
        'Points': 10
    }
    
    ]
}

#create list of formations
#formations = [[5,4,1],[5,3,2],[4,4,2],[4,3,3],[3,5,2],[3,4,3]]
#scaled down to one formation for intial development
formations = [[3,5,2]]

#For each formation, calculate minimum budget needed for the bench.
squad_price = 0
budget = 100
min_GK_price = 4.0
min_DF_price = 4.0
min_MD_price = 4.5
min_FD_price = 4.5

bench_GK = 1
bench_DF = 5 - formations[0][0]
bench_MD = 5 - formations[0][1]
bench_FD = 3 - formations[0][2]

min_bench_budget = bench_GK * min_GK_price + bench_DF * min_DF_price + bench_MD * min_MD_price + bench_FD * min_FD_price

#And budget for starting XI
starting_XI_budget = budget - min_bench_budget

#declare variables for using in nested loops below
results = {'Points': 0, 'Starting_XI': '', 'Cost': starting_XI_budget}
combinations_tested = 0

#loop through each combination of players
for gk in players['GK']: #for each GK
    clubs = {'Arsenal': 0, 'Crystal Palace': 0, 'Chelsea': 0, 'Everton': 0} #...
    for a in range(0,len(players['DEF']) - 2):
        for b in range(a+1,len(players['DEF']) - 1):
            for c in range(b+1,len(players['DEF'])):
                for d in range(0,len(players['MID']) - 4):
                    for e in range(d + 1, len(players['MID']) - 3):
                        for f in range(e + 1, len(players['MID']) - 2):
                            for g in range(f + 1, len(players['MID']) - 2):
                                for h in range(g + 1, len(players['MID'])):
                                    for i in range(0, len(players['FWD']) - 1):
                                        for j in range(i + 1, len(players['FWD'])):
                                            combinations_tested += 1

                                            #check if total points of XI higher than default/current toal
                                            points = gk['Points'] + players['DEF'][a]['Points'] + players['DEF'][b]['Points'] + players['DEF'][c]['Points'] + players['MID'][d]['Points'] + players['MID'][e]['Points'] + players['MID'][f]['Points'] + players['MID'][g]['Points'] + players['MID'][h]['Points'] + players['FWD'][i]['Points'] + players['FWD'][j]['Points']
                                            if points >= results['Points']:
                                                #now check cost - if wanted to return both teams that have equal pionts and price. could have elif: append
                                                cost = gk['Price'] + players['DEF'][a]['Price'] + players['DEF'][b]['Price'] + players['DEF'][c]['Price'] + players['MID'][d]['Price'] + players['MID'][e]['Price'] + players['MID'][f]['Price'] + players['MID'][g]['Price'] + players['MID'][h]['Price'] + players['FWD'][i]['Price'] + players['FWD'][j]['Price']
                                                if cost <= results['Cost']:
                                                    #add check here for clubs played for

                                                    #get player names and add all data to results{}
                                                    starting_XI = [gk['Name'], players['DEF'][a]['Name'], players['DEF'][b]['Name'], players['DEF'][c]['Name'], players['MID'][d]['Name'], players['MID'][e]['Name'], players['MID'][f]['Name'], players['MID'][g]['Name'], players['MID'][h]['Name'], players['FWD'][i]['Name'], players['FWD'][j]['Name']]
                                                    results['Starting_XI'] = starting_XI
                                                    results['Points'] = points
                                                    results['Cost'] = cost
pprint(results)
print('Combinations tested: ' + str(combinations_tested))

#fill bench - select best players at lowest price piont for each empty position where player per team limit is not exceeded
#determine bench order - order by average predicted pionts/value or by enforced substitutions?

#find best player for position one

#repeat for positions 2-3