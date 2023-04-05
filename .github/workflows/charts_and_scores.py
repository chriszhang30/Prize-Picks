# plotting probability scores #
### Plotting Charts of Highest Scores ###
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(20,10))
sns.set(style="whitegrid", color_codes=True)

# Over Probability Scores #
data = stats_df[stats_df['Over Score']>=0.7][['Player + Line','Over Score']].sort_values(by=['Over Score'], ascending=False) # data underlying bar plot in question

pal = sns.color_palette("Greens_d", len(data))
rank = data['Over Score'].argsort().argsort()  # http://stackoverflow.com/a/6266510/1628638
sns.barplot(x=data['Player + Line'], y=data['Over Score'], palette=np.array(pal)[rank])
plt.xticks(rotation=90)

plt.show()


# Under Probability Scores #
plt.figure(figsize=(20,10))
sns.set(style="whitegrid", color_codes=True)

data = stats_df[stats_df['Under Score']>=0.7][['Player + Line','Under Score']].sort_values(by=['Under Score'], ascending=False) # data underlying bar plot in question

pal = sns.color_palette("Greens_d", len(data))
rank = data['Under Score'].argsort().argsort()  # http://stackoverflow.com/a/6266510/1628638
sns.barplot(x=data['Player + Line'], y=data['Under Score'], palette=np.array(pal)[rank])
plt.xticks(rotation=90)

plt.show()


### Plotting Heat Map of Highest Prob and Over/Under Scores to Identify Best Picks ###
# Heatmaps to display best picks #
data = stats_df[stats_df['Over Score']>=0.7][['Over Score', 'Over Amount Score']].sort_values(by=['Over Score', 'Over Amount Score'])
  
# plotting the heatmap
hm = sns.heatmap(data=data, annot=True, cmap="Reds")
plt.show()

# Heatmaps to display best picks #
data = stats_df[stats_df['Under Score']>=0.7][['Under Score', 'Under Amount Score']].sort_values(by=['Under Score', 'Under Amount Score'])
  
# plotting the heatmap
hm = sns.heatmap(data=data, annot=True, cmap="Blues")
plt.show()



# Detailed Table Output for Analysis #
highest_overs = stats_df[stats_df['Over Score']>=0.7][['Player + Line','Over Score', 'Over Amount Score',
                                                 'Overall % Over','L5 % Over','L10 % Over','L15 % Over','L20 % Over', 
                                                 'L5 Over Avg', 'L10 Over Avg', 'L15 Over Avg', 'L20 Over Avg']].sort_values(by=['Over Score'], ascending=False)

highest_unders = stats_df[stats_df['Under Score']>=0.7][['Player + Line','Under Score', 'Under Amount Score',
                                                 'Overall % Under','L5 % Under','L10 % Under','L15 % Under','L20 % Under', 
                                                 'L5 Under Avg', 'L10 Under Avg', 'L15 Under Avg', 'L20 Under Avg']].sort_values(by=['Under Score'], ascending=False)


# Looking for Hottest and Coldest Players #
# Last 5 games are they always over, last 5 games are they always under #
stats_df[stats_df['L5 % Over']>=0.8].sort_values(by=['L5 % Over', 'L5 Over Avg'],ascending=False)
stats_df[stats_df['L5 % Under']>=0.8].sort_values(by=['L5 % Under', 'L5 Under Avg'],ascending=False)

