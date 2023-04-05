from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
import pandas as pd 


from nba_api.stats.static import players

#players we want to look into
pp_players = pp['attributes.name'].unique()

#initialize empty lists that will put player id into
player_ids = []
for i in pp_players:
    player_ids.append(players.find_players_by_full_name(i)[0]['id'])
    

#pull game logs of each player
game_logs =[]
for i in player_ids:
    game_logs.append(playergamelog.PlayerGameLog(player_id=i, season = '2022-23').get_data_frames()[0])

player_data = dict(zip(pp_players, game_logs))

#Enter any player from superstar list to access their game log
# df = player_data["Aaron Nesmith"]



def pp_multi_stat(df):
    df['PTS+REB+AST'] = df['PTS']+df['REB']+df['AST']
    df['PTS+REB'] = df['PTS']+df['REB']
    df['PTS+AST'] = df['PTS']+df['AST']
    df['REB+AST'] = df['REB']+df['AST']
    df['BLK+STL'] = df['BLK']+df['STL']
    df['FPTS'] = df['PTS']+1.2*df['REB']+1.5*df['AST']+3*df['BLK']+3*df['STL']-1*df['TOV']
    
    return df
    
    
 def return_stats(df,player_name,stat,line):
    
    mu = np.mean(df[stat])  # mean of distribution
    sigma = np.std(df[stat])  # standard deviation of distribution
    x = df[stat]

    pp_line = str(line) + ' ' + stat

    # num_bins = 15

    #calculate probabilities
    overall_over = sum(x>line) / len(x)
    l5_over = sum(x.head(5)>line) / len(x.head(5))
    l10_over = sum(x.head(10)>line) / len(x.head(10))
    l15_over = sum(x.head(15)>line) / len(x.head(15))
    l20_over = sum(x.head(20)>line) / len(x.head(20))
    l5_over_avg = sum(x.head(5) - line) / len(x.head(5))
    l10_over_avg = sum(x.head(10) - line) / len(x.head(10))
    l15_over_avg = sum(x.head(15) - line) / len(x.head(15))
    l20_over_avg = sum(x.head(20) - line) / len(x.head(20))
    overall_over_avg = sum(x - line) / len(x)


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
    
    over_score = (overall_over + l5_over + l10_over + l15_over + l20_over) / 5
    under_score = (overall_under + l5_under + l10_under + l15_under + l20_under) / 5
    
    over_amount_score = (l5_over_avg + l10_over_avg + l15_over_avg + l20_over_avg) / 4
    under_amount_score = (l5_under_avg + l10_under_avg + l15_under_avg + l20_under_avg) / 4

    arr = [[player_name, pp_line, mu, overall_over, l5_over, l10_over, l15_over, l20_over, overall_under, l5_under, l10_under, l15_under, l20_under,
            l5_over_avg, l10_over_avg, l15_over_avg, l20_over_avg, overall_over_avg, l5_under_avg, l10_under_avg, l15_under_avg, l20_under_avg, overall_under_avg,
            over_score, over_amount_score, under_score, under_amount_score]]

    return arr
    
 
 import numpy as np

pp_cols = ['Player', 'Line', 'Season Avg', 'Overall % Over', 'L5 % Over', 'L10 % Over', 'L15 % Over', 'L20 % Over',
           'Overall % Under', 'L5 % Under', 'L10 % Under', 'L15 % Under', 'L20 % Under', 'L5 Over Avg', 'L10 Over Avg',
           'L15 Over Avg', 'L20 Over Avg', 'Overall Over Avg', 'L5 Under Avg', 'L10 Under Avg', 'L15 Under Avg', 
           'L20 Under Avg', 'Overall Under Avg', 'Over Score', 'Over Avg Score', 'Under Score', 'Under Avg Score']

stats_df = pd.DataFrame(columns=pp_cols)

for player in pp_players:
    lines = pp[pp['attributes.name']==player][['game_stat','attributes.line_score']].set_index('game_stat').T.to_dict('list')
    logs = pp_multi_stat(player_data[player])
    
    for stat in lines:
        arr = return_stats(logs, player, stat, lines[stat][0])
        stats_df = pd.concat([stats_df, pd.DataFrame(arr, columns=pp_cols)], ignore_index=True)
