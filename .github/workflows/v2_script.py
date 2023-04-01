import pandas as pd
import numpy as np


def pull_box_score_realgm(url):
  # pull box scores from RealGM with input game logs url for player
  
    df = pd.read_html(url)[4]
    df = df[df['Date']!='Totals']
    df = df[df['Date']!='Averages']
    
#     df = df[df['Team']=='Clippers']

   
    df['PTS'] = df['PTS'].astype(float)
    df['REB'] = df['REB'].astype(float)
    df['AST'] = df['AST'].astype(float)
    df['PTS+REB+AST'] = df['PTS']+df['REB']+df['AST']
    df['PTS+REB'] = df['PTS']+df['REB']
    df['PTS+AST'] = df['PTS']+df['AST']
    df['REB+AST'] = df['REB']+df['AST']
    df['3P'] = df['3PM'].astype(float)
    df['BLK'] = df['BLK'].astype(float)
    df['STL'] = df['STL'].astype(float)
    df['BLK+STL'] = df['BLK']+df['STL']
    df['TOV'] = df['TOV'].astype(float)
    df['FT'] = df['FTM'].astype(float)
   
    return df
  
def return_stats_realgm(player_name,url,stat,line):
    df = pull_box_score_realgm(url)
    
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

    arr = [[player_name, pp_line, mu, overall_over, l5_over, l10_over, l15_over, l20_over, overall_under, l5_under, l10_under, l15_under, l20_under,
            l5_over_avg, l10_over_avg, l15_over_avg, l20_over_avg, overall_over_avg, l5_under_avg, l10_under_avg, l15_under_avg, l20_under_avg, overall_under_avg]]

    return arr
  

  # create the data frame #
pp_cols = ['Player','Line','Season Avg','Overall % Over', 'L5 % Over', 'L10 % Over', 'L15 % Over', 'L20 % Over',
           'Overall % Under', 'L5 % Under', 'L10 % Under', 'L15 % Under', 'L20 % Under',
           'L5 Over Avg', 'L10 Over Avg', 'L15 Over Avg', 'L20 Over Avg', 'Overall Over Avg',
           'L5 Under Avg', 'L10 Under Avg', 'L15 Under Avg', 'L20 Under Avg', 'Overall Under Avg']

realgm_df = pd.DataFrame(columns=pp_cols)


# examples #
lines = {'PTS':8.5, 'PTS+REB+AST':12.5, 'PTS+REB':10.5, 'PTS+AST':10.5, '3P':1.5}
url = 'https://basketball.realgm.com/player/Gabe-Vincent/GameLogs/80552'
name = 'Gabe Vincent'

for stat in lines:
    realgm_df = pd.concat([realgm_df, pd.DataFrame(return_stats_realgm(name,url,stat,lines[stat]),columns=pp_cols)], ignore_index=True)
    
lines = {'PTS':24.5, 'REB':6.0, 'AST':5.0, 'PTS+REB+AST':36.5, 'PTS+REB':30.5, 'PTS+AST':29.5, 'REB+AST':11.5}
url = 'https://basketball.realgm.com/player/Jimmy-Butler/GameLogs/6160'
name = 'Jimmy Butler'

for stat in lines:
    realgm_df = pd.concat([realgm_df, pd.DataFrame(return_stats_realgm(name,url,stat,lines[stat]),columns=pp_cols)], ignore_index=True)
    
lines = {'PTS+REB+AST':7.5, 'BLK+STL':0.5, 'TOV':0.5}
url = 'https://basketball.realgm.com/player/Dwight-Powell/GameLogs/9346'
name = 'Dwight Powell'

for stat in lines:
    realgm_df = pd.concat([realgm_df, pd.DataFrame(return_stats_realgm(name,url,stat,lines[stat]),columns=pp_cols)], ignore_index=True)
    
    
    
### Calculating Scores for Over and Under Probabilities ###
def calculate_scores(pp_df):

    pp_df['Season Avg'] = pp_df['Season Avg'].astype(float)
    pp_df['Overall % Over'] = pp_df['Overall % Over'].astype(float)
    pp_df['L5 % Over'] = pp_df['L5 % Over'].astype(float)
    pp_df['L10 % Over'] = pp_df['L10 % Over'].astype(float)
    pp_df['L15 % Over'] = pp_df['L15 % Over'].astype(float)
    pp_df['L20 % Over'] = pp_df['L20 % Over'].astype(float)
    pp_df['Overall % Under'] = pp_df['Overall % Under'].astype(float)
    pp_df['L5 % Under'] = pp_df['L5 % Under'].astype(float)
    pp_df['L10 % Under'] = pp_df['L10 % Under'].astype(float)
    pp_df['L15 % Under'] = pp_df['L15 % Under'].astype(float)
    pp_df['L20 % Under'] = pp_df['L20 % Under'].astype(float)

    pp_df['L5 Over Avg'] = pp_df['L5 Over Avg'].astype(float)
    pp_df['L10 Over Avg'] = pp_df['L10 Over Avg'].astype(float)
    pp_df['L15 Over Avg'] = pp_df['L15 Over Avg'].astype(float)
    pp_df['L20 Over Avg'] = pp_df['L20 Over Avg'].astype(float)
    pp_df['Overall Over Avg'] = pp_df['Overall Over Avg'].astype(float)

    pp_df['L5 Under Avg'] = pp_df['L5 Under Avg'].astype(float)
    pp_df['L10 Under Avg'] = pp_df['L10 Under Avg'].astype(float)
    pp_df['L15 Under Avg'] = pp_df['L15 Under Avg'].astype(float)
    pp_df['L20 Under Avg'] = pp_df['L20 Under Avg'].astype(float)
    pp_df['Overall Under Avg'] = pp_df['Overall Under Avg'].astype(float)


    pp_df['Over Score'] = (pp_df['Overall % Over'] + pp_df['L5 % Over'] + pp_df['L10 % Over'] + pp_df['L15 % Over'] + pp_df['L20 % Over']) / 5
    pp_df['Under Score'] = (pp_df['Overall % Under'] + pp_df['L5 % Under'] + pp_df['L10 % Under'] + pp_df['L15 % Under'] + pp_df['L20 % Under']) / 5

    pp_df['Under Amount Score'] = (pp_df['L5 Under Avg'] + pp_df['L10 Under Avg'] + pp_df['L15 Under Avg'] + pp_df['L20 Under Avg']) / 4
    pp_df['Over Amount Score'] = (pp_df['L5 Over Avg'] + pp_df['L10 Over Avg'] + pp_df['L15 Over Avg'] + pp_df['L20 Over Avg']) / 4


    pp_df['Player + Line'] = pp_df['Player'] + ' ' + pp_df['Line']
    
    return pp_df
  
realgm_df = calculate_scores(realgm_df)


# plotting probability scores #
### Plotting Charts of Highest Scores ###
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(20,10))
sns.set(style="whitegrid", color_codes=True)

# Over Probability Scores #
data = realgm_df[realgm_df['Over Score']>=0.5][['Player + Line','Over Score']].sort_values(by=['Over Score'], ascending=False) # data underlying bar plot in question

pal = sns.color_palette("Greens_d", len(data))
rank = data['Over Score'].argsort().argsort()  # http://stackoverflow.com/a/6266510/1628638
sns.barplot(x=data['Player + Line'], y=data['Over Score'], palette=np.array(pal)[rank])
plt.xticks(rotation=90)

plt.show()

# Under Probability Scores #
plt.figure(figsize=(20,10))
sns.set(style="whitegrid", color_codes=True)

data = realgm_df[realgm_df['Under Score']>=0.5][['Player + Line','Under Score']].sort_values(by=['Under Score'], ascending=False) # data underlying bar plot in question

pal = sns.color_palette("Greens_d", len(data))
rank = data['Under Score'].argsort().argsort()  # http://stackoverflow.com/a/6266510/1628638
sns.barplot(x=data['Player + Line'], y=data['Under Score'], palette=np.array(pal)[rank])
plt.xticks(rotation=90)

plt.show()



### Plotting Heat Map of Highest Prob and Over/Under Scores to Identify Best Picks ###
# Heatmaps to display best picks #
data = realgm_df[realgm_df['Over Score']>=0.6][['Over Score', 'Over Amount Score']].sort_values(by=['Over Score', 'Over Amount Score'])
  
# plotting the heatmap
hm = sns.heatmap(data=data, annot=True, cmap=sns.cubehelix_palette(as_cmap=True))
plt.show()

# Heatmaps to display best picks #
data = realgm_df[realgm_df['Under Score']>=0.6][['Under Score', 'Under Amount Score']].sort_values(by=['Under Score', 'Under Amount Score'])
  
# plotting the heatmap
hm = sns.heatmap(data=data, annot=True, cmap=sns.cubehelix_palette(as_cmap=True))
plt.show()


# Detailed Table Output for Analysis #
highest_overs = realgm_df[realgm_df['Over Score']>=0.6][['Player + Line','Over Score', 'Over Amount Score',
                                                 'Overall % Over','L5 % Over','L10 % Over','L15 % Over','L20 % Over', 
                                                 'L5 Over Avg', 'L10 Over Avg', 'L15 Over Avg', 'L20 Over Avg']].sort_values(by=['Over Score'], ascending=False)

highest_unders = realgm_df[realgm_df['Under Score']>=0.6][['Player + Line','Under Score', 'Under Amount Score',
                                                 'Overall % Under','L5 % Under','L10 % Under','L15 % Under','L20 % Under', 
                                                 'L5 Under Avg', 'L10 Under Avg', 'L15 Under Avg', 'L20 Under Avg']].sort_values(by=['Under Score'], ascending=False)
