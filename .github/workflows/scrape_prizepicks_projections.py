import pandas as pd
import requests

params = (
    ('league', 'NBA'),
    ('single_stat', 'true'),
)
headers = {
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

}

session = requests.Session() 
response = session.get('https://api.prizepicks.com/projections', data=params, headers=headers)

df1 = pd.json_normalize(response.json()['included'])
df1 = df1[df1['type'] == 'new_player']

df2 = pd.json_normalize(response.json()['data'])

df = pd.DataFrame(zip(df1['attributes.name'], df2['attributes.stat_type'], df2['attributes.line_score']), columns=['name', 'stat', 'line'])

nba_names = df1[df1['attributes.league']=='NBA']

nba_proj = df2[df2['relationships.league.data.id']=='7']

new_df = pd.merge(nba_names, nba_proj,  how='inner', left_on=['id'], right_on = ['relationships.new_player.data.id'])
new_df[['attributes.league', 'attributes.league_id', 'attributes.team', 'attributes.name', 'attributes.line_score', 'attributes.stat_type']]

stat_map = {'Pts+Rebs+Asts':'PTS+REB+AST', 'Assists':'AST', 'Rebounds':'REB', 'Points':'PTS', 'Pts+Asts':'PTS+AST', 'Pts+Rebs':'PTS+REB', 
            'Rebs+Asts':'REB+AST', '3-PT Made':'3P', 'Free Throws Made':'FT', 'Fantasy Score':'FPTS'}

new_df['game_stat'] = new_df['attributes.stat_type'].map(stat_map)
new_df[['attributes.league', 'attributes.league_id', 'attributes.team', 'attributes.name', 'attributes.line_score', 'game_stat']]
