import pandas as pd
import numpy as np


def pull_box_score(url):
  # pull box scores from Basketball Reference with input game logs url for player
  
    df = pd.read_html(url)[7]
    df = df[df['GS']!='Inactive']
    df = df[df['GS']!='Did Not Dress']
    df = df[df['GS']!='Not With Team']
    df = df[df['GS']!='Did Not Play']
    df = df[df['PTS']!='PTS']
    df = df[df['PTS']!='Player Suspended']

   
    df['PTS'] = df['PTS'].astype(float)
    df['TRB'] = df['TRB'].astype(float)
    df['AST'] = df['AST'].astype(float)
    df['PTS+REB+AST'] = df['PTS']+df['TRB']+df['AST']
    df['PTS+REB'] = df['PTS']+df['TRB']
    df['PTS+AST'] = df['PTS']+df['AST']
    df['REB+AST'] = df['TRB']+df['AST']
    df['3P'] = df['3P'].astype(float)
    df['BLK'] = df['BLK'].astype(float)
    df['STL'] = df['STL'].astype(float)
    df['BLK+STL'] = df['BLK']+df['STL']
    df['TOV'] = df['TOV'].astype(float)
    df['FT'] = df['FT'].astype(float)
   
    return df
  
def return_stats_2(player_name,df,stat,line):

    # grab player name from url
    # import requests
    # page = requests.get(url)

    # from bs4 import BeautifulSoup
    # soup = BeautifulSoup(page.content, "html.parser")

    # results = soup.find(id="info", class_="players")
    # player_span = str(results.find("span"))
    # player_name = player_span[6:-24]

    # grab player stats
    # logs = pull_box_score(url).sort_values(by=['Date'])
    mu = np.mean(df[stat])  # mean of distribution
    sigma = np.std(df[stat])  # standard deviation of distribution
    x = df[stat]

    pp_line = str(line) + ' ' + stat

    # num_bins = 15

    #calculate probabilities
    overall_over = sum(x>line) / len(x)
    l5_over = sum(x.tail(5)>line) / len(x.tail(5))
    l10_over = sum(x.tail(10)>line) / len(x.tail(10))
    l15_over = sum(x.tail(15)>line) / len(x.tail(15))
    l20_over = sum(x.tail(20)>line) / len(x.tail(20))
    l5_over_avg = sum(x.tail(5) - line) / len(x.tail(5))
    l10_over_avg = sum(x.tail(10) - line) / len(x.tail(10))
    l15_over_avg = sum(x.tail(15) - line) / len(x.tail(15))
    l20_over_avg = sum(x.tail(20) - line) / len(x.tail(20))
    overall_over_avg = sum(x - line) / len(x)


    overall_under = sum(x<line) / len(x)
    l5_under = sum(x.tail(5)<line) / len(x.tail(5))
    l10_under = sum(x.tail(10)<line) / len(x.tail(10))
    l15_under = sum(x.tail(15)<line) / len(x.tail(15))
    l20_under = sum(x.tail(20)<line) / len(x.tail(20))
    l5_under_avg = sum(line - x.tail(5)) / len(x.tail(5))
    l10_under_avg = sum(line - x.tail(10)) / len(x.tail(10))
    l15_under_avg = sum(line - x.tail(15)) / len(x.tail(15))
    l20_under_avg = sum(line - x.tail(20)) / len(x.tail(20))
    overall_under_avg = sum(line - x) / len(x)

    arr = [[player_name, pp_line, mu, overall_over, l5_over, l10_over, l15_over, l20_over, overall_under, l5_under, l10_under, l15_under, l20_under,
            l5_over_avg, l10_over_avg, l15_over_avg, l20_over_avg, overall_over_avg, l5_under_avg, l10_under_avg, l15_under_avg, l20_under_avg, overall_under_avg]]

#     fig, ax = plt.subplots()

#     # the histogram of the data
#     n, bins, patches = ax.hist(x, num_bins, density=1)

#     # add a 'best fit' line
#     y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
#          np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
#     ax.plot(bins, y, '--')
#     ax.set_xlabel('Smarts')
#     ax.set_ylabel('Probability density')
#     ax.set_title(r'Histogram of IQ: $\mu={mu}$, $\sigma={sigma}$')

    # Tweak spacing to prevent clipping of ylabel
#     fig.tight_layout()
#     plt.show()
   
    # print('Overall Prob: ' + str(sum(x>line) / len(x)))
    # print('Last 5 Prob:' + str(sum(x.tail(5)>line) / len(x.tail(5))))
    # print('Last 10 Prob:' + str(sum(x.tail(10)>line) / len(x.tail(10))))
    # print('Last 15 Prob:' + str(sum(x.tail(15)>line) / len(x.tail(15))))
    # print('Last 20 Prob:' + str(sum(x.tail(20)>line) / len(x.tail(20))))

    return arr



### Examples (currently have to manually do all, need PrizePicks API and a better way to pull game logs, since Basketball Reference blocks your access if you pull too many too quickly ###

# Trae Young - 3/31/23 #
trae_url = 'https://www.basketball-reference.com/players/y/youngtr01/gamelog/2023'
pp_cols = ['Player','Line','Season Avg','Overall % Over', 'L5 % Over', 'L10 % Over', 'L15 % Over', 'L20 % Over',
           'Overall % Under', 'L5 % Under', 'L10 % Under', 'L15 % Under', 'L20 % Under']

pp_df = pd.DataFrame(columns=['Player','Line','Season Avg','Overall % Over', 'L5 % Over', 'L10 % Over', 'L15 % Over', 'L20 % Over',
                                      'Overall % Under', 'L5 % Under', 'L10 % Under', 'L15 % Under', 'L20 % Under'])

logs = pull_box_score(trae_url).sort_values(by=['Date'])                              
player = 'Trae Young'

pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'PTS', 26.0), columns=pp_cols)], ignore_index = True)
# pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'TRB', 4.0), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'AST', 9.5), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'PTS+REB+AST', 38.5), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'PTS+REB', 28.5), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'PTS+AST', 35.5), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'REB+AST', 12.5), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'FT', 7.5), columns=pp_cols)], ignore_index = True)


# Mikal Bridges - 3/31/23 #
mikal_url = 'https://www.basketball-reference.com/players/b/bridgmi01/gamelog/2023'

logs = pull_box_score(mikal_url).sort_values(by=['Date'])       
logs = logs[logs['Tm']=='BRK']                        
player = 'Mikal Bridges'

pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'PTS', 27.5), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'TRB', 4.0), columns=pp_cols)], ignore_index = True)
# pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'AST', 9.5), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'PTS+REB+AST', 34.5), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, '3P', 2.5), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'PTS+REB', 31.5), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'PTS+AST', 30.5), columns=pp_cols)], ignore_index = True)
# pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'REB+AST', 12.5), columns=pp_cols)], ignore_index = True)
pp_df = pd.concat([pp_df, pd.DataFrame(return_stats_2(player, logs, 'FT', 6.5), columns=pp_cols)], ignore_index = True)


### Calculating Scores for Over and Under Probabilities ###
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

pp_df['Over Score'] = (pp_df['Overall % Over'] + pp_df['L5 % Over'] + pp_df['L10 % Over'] + pp_df['L15 % Over'] + pp_df['L20 % Over']) / 5
pp_df['Under Score'] = (pp_df['Overall % Under'] + pp_df['L5 % Under'] + pp_df['L10 % Under'] + pp_df['L15 % Under'] + pp_df['L20 % Under']) / 5

pp_df['Player + Line'] = pp_df['Player'] + ' ' + pp_df['Line']


### Plotting Charts of Highest Scores ###
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(20,10))
sns.set(style="whitegrid", color_codes=True)

# Over Probability Scores #
data = pp_df[pp_df['Over Score']>=0.7][['Player + Line','Over Score']].sort_values(by=['Over Score'], ascending=False) # data underlying bar plot in question

pal = sns.color_palette("Greens_d", len(data))
rank = data['Over Score'].argsort().argsort()  # http://stackoverflow.com/a/6266510/1628638
sns.barplot(x=data['Player + Line'], y=data['Over Score'], palette=np.array(pal)[rank])
plt.xticks(rotation=90)

plt.show()

# Under Probability Scores #
plt.figure(figsize=(20,10))
sns.set(style="whitegrid", color_codes=True)

data = pp_df[pp_df['Under Score']>=0.7][['Player + Line','Under Score']].sort_values(by=['Under Score'], ascending=False) # data underlying bar plot in question

pal = sns.color_palette("Greens_d", len(data))
rank = data['Under Score'].argsort().argsort()  # http://stackoverflow.com/a/6266510/1628638
sns.barplot(x=data['Player + Line'], y=data['Under Score'], palette=np.array(pal)[rank])
plt.xticks(rotation=90)

plt.show()

# Detailed Table Output for Analysis #
highest_overs = pp_df[pp_df['Over Score']>=0.68][['Player + Line','Over Score','Overall % Over','L5 % Over','L10 % Over','L15 % Over','L20 % Over']].sort_values(by=['Over Score'], ascending=False)

highest_unders = pp_df[pp_df['Under Score']>=0.7][['Player + Line','Under Score','Overall % Under','L5 % Under','L10 % Under','L15 % Under','L20 % Under']].sort_values(by=['Under Score'], ascending=False)


# Heatmaps to display best picks #
import seaborn as sns

vmin = 0
vmax = 1

data = pp_df[pp_df['Over Score']>=0.7][['Over Score', 'Over Amount Score']].sort_values(by=['Over Score', 'Over Amount Score'])
  
# plotting the heatmap
hm = sns.heatmap(data=data, annot=True, cmap=sns.cubehelix_palette(as_cmap=True))


import seaborn as sns

vmin = 0
vmax = 1

data = pp_df[pp_df['Under Score']>=0.7][['Under Score', 'Under Amount Score']].sort_values(by=['Under Score', 'Under Amount Score'])
  
# plotting the heatmap
hm = sns.heatmap(data=data, annot=True, cmap=sns.cubehelix_palette(as_cmap=True))
