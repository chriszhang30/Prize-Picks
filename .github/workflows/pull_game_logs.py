from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
import pandas as pd 


from nba_api.stats.static import players

# running list of player names that don't exactly match between PrizePicks and NBA API -- change PrizePicks names to ones in NBA API
new_df = new_df.replace('Nicolas Claxton', 'Nic Claxton')
new_df = new_df.replace('OG Anunoby', 'O.G. Anunoby')
new_df = new_df.replace('Fred VanVleet\t', 'Fred VanVleet')

#players we want to look into
pp_players = new_df['attributes.name'].unique()

#initialize empty lists that will put player id into
player_ids = []
for i in pp_players:
    player_ids.append(players.find_players_by_full_name(i)[0]['id']) #this will error out if it finds a name that doesn't match
    
# if this errors out, compare the output of follinwg two to find where the error is
# dict(zip(pp_players, player_ids))
# pp_players

#pull game logs of each player
game_logs =[]
for i in player_ids:
    game_logs.append(playergamelog.PlayerGameLog(player_id=i, season = '2022-23').get_data_frames()[0])
    sleep(1) # to ensure NBA API doesn't block you lol

player_data = dict(zip(pp_players, game_logs))
