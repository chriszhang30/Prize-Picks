 import numpy as np
 import pandas as pd
  
def pp_multi_stat(df):
  # creates the prizepick multi-stat categories from game logs and renames some boxscore stat names to match with prizepick stat names
  df['PTS+REB+AST'] = df['PTS']+df['REB']+df['AST']
  df['PTS+REB'] = df['PTS']+df['REB']
  df['PTS+AST'] = df['PTS']+df['AST']
  df['REB+AST'] = df['REB']+df['AST']
  df['BLK+STL'] = df['BLK']+df['STL']
  df['FPTS'] = df['PTS']+1.2*df['REB']+1.5*df['AST']+3*df['BLK']+3*df['STL']-1*df['TOV']
  df['3P'] = df['FG3M']
  df['FT'] = df['FTM']
  
def return_stats(df,player_name,stat,line):
    # provide function the dataframe with players game logs, player name, and prizepicks projections (e.g. stat = PTS, line = 23.5)
    
    mu = np.mean(df[stat])  # mean of distribution
    sigma = np.std(df[stat])  # standard deviation of distribution -- not in use yet
    x = df[stat] # use this to calculate probabilities

    pp_line = str(line) + ' ' + stat

    #calculate probabilities
    overall_over = sum(x>line) / len(x) #overall probability of going over
    l5_over = sum(x.head(5)>line) / len(x.head(5)) #last 5 game probability of going over
    l10_over = sum(x.head(10)>line) / len(x.head(10)) # last 10 game probability of going over
    l15_over = sum(x.head(15)>line) / len(x.head(15)) #last 15 game probability of going over
    l20_over = sum(x.head(20)>line) / len(x.head(20)) #last 20 game probability of going over
    l5_over_avg = sum(x.head(5) - line) / len(x.head(5)) #last 5 game average difference between actual and prizepick line
    l10_over_avg = sum(x.head(10) - line) / len(x.head(10)) #last 10 game average difference between actual and prizepick line
    l15_over_avg = sum(x.head(15) - line) / len(x.head(15)) #last 15 game average difference between actual and prizepick line
    l20_over_avg = sum(x.head(20) - line) / len(x.head(20)) #last 20 game average difference between actual and prizepick line
    overall_over_avg = sum(x - line) / len(x) #overall average difference between actual and prizepick line

    # same thing as above but for probabilites and avgs of going under the projection
    overall_under = sum(x<line) / len(x)
    l5_under = sum(x.head(5)<line) / len(x.head(5))
    l10_under = sum(x.head(10)<line) / len(x.head(10))
    l15_under = sum(x.head(15)<line) / len(x.head(15))
    l20_under = sum(x.head(20)<line) / len(x.head(20))
    l5_under_avg = sum(line - x.head(5)) / len(x.head(5))
    l10_under_avg = sum(line - x.head(10)) / len(x.head(10))
    l15_under_avg = sum(line - x.head(15)) / len(x.head(15))
    l20_under_avg = sum(line - x.head(20)) / len(x.head(20))
    overall_under_avg = sum(line - x) / len(x)
    
    # calculating a probability "score" -- simply the average of overall, L5, L10, L15 and L20
    over_score = (overall_over + l5_over + l10_over + l15_over + l20_over) / 5
    under_score = (overall_under + l5_under + l10_under + l15_under + l20_under) / 5
    
    # calculating an over/under amount "score" -- this is to take into account which high probability scoring ones are more/less risky
    # higher score means less risky, lower score means more risky (more prone to luck)
    over_amount_score = (l5_over_avg + l10_over_avg + l15_over_avg + l20_over_avg) / 4
    under_amount_score = (l5_under_avg + l10_under_avg + l15_under_avg + l20_under_avg) / 4

    arr = [[player_name, pp_line, mu, overall_over, l5_over, l10_over, l15_over, l20_over, overall_under, l5_under, l10_under, l15_under, l20_under,
            l5_over_avg, l10_over_avg, l15_over_avg, l20_over_avg, overall_over_avg, l5_under_avg, l10_under_avg, l15_under_avg, l20_under_avg, overall_under_avg,
            over_score, over_amount_score, under_score, under_amount_score]]

    return arr

  


# create the final dataframe
pp_cols = ['Player', 'Line', 'Season Avg', 'Overall % Over', 'L5 % Over', 'L10 % Over', 'L15 % Over', 'L20 % Over',
           'Overall % Under', 'L5 % Under', 'L10 % Under', 'L15 % Under', 'L20 % Under', 'L5 Over Avg', 'L10 Over Avg',
           'L15 Over Avg', 'L20 Over Avg', 'Overall Over Avg', 'L5 Under Avg', 'L10 Under Avg', 'L15 Under Avg', 
           'L20 Under Avg', 'Overall Under Avg', 'Over Score', 'Over Avg Score', 'Under Score', 'Under Avg Score']

stats_df = pd.DataFrame(columns=pp_cols)

# loop through all the players in the PrizePicks pull
for player in pp_players:
    lines = pp[pp['attributes.name']==player][['game_stat','attributes.line_score']].set_index('game_stat').T.to_dict('list') #creates dictionary of player's projections
    logs = pp_multi_stat(player_data[player]) # game log matching with prizepick stats
    
    # to take into account players traded during season to filter for only most recent team 
    most_recent_team = logs.head(1).MATCHUP.str.slice(start=0, stop=3, step=1)[0]
    logs = logs[logs.MATCHUP.str.slice(start=0, stop=3, step=1)==most_recent_team
    
    # loop through each PrizePick projection to calculate stats and scores
    for stat in lines:
        arr = return_stats(logs, player, stat, lines[stat][0])
        stats_df = pd.concat([stats_df, pd.DataFrame(arr, columns=pp_cols)], ignore_index=True) 
