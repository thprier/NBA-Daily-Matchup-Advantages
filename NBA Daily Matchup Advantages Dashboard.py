#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from nba_api.stats.static import teams
from nba_api.stats.endpoints import Scoreboard
from nba_api.stats.endpoints import synergyplaytypes
import datetime

#Part 1: Getting list of today's NBA matchups

# Get a list of all NBA teams and their information
nba_teams = teams.get_teams()

# Extract team abbreviations
team_abbreviations = [team['abbreviation'] for team in nba_teams]

# Create a DataFrame with the desired column name
team_df = pd.DataFrame({'TEAM_ABBREVIATION': team_abbreviations, 'Opponent': ''}, dtype=object)

# Get today's date
today = datetime.date.today()

# Define the parameters for the Scoreboard API
game_date = today.strftime("%Y-%m-%d")
league_id = "00"  # 00 stands for the NBA

# Create the Scoreboard API instance
scoreboard = Scoreboard(game_date=game_date, league_id=league_id)

# Get today's games data
games_data = scoreboard.get_data_frames()[0]

# Iterate through the games and add opponent information to the DataFrame
for _, game in games_data.iterrows():
    home_team = game['HOME_TEAM_ID']
    away_team = game['VISITOR_TEAM_ID']

    home_team_abbreviation = teams.find_team_name_by_id(home_team)['abbreviation']
    away_team_abbreviation = teams.find_team_name_by_id(away_team)['abbreviation']

    # Find the corresponding row for each team and add the opponent
    home_team_row = team_df[team_df['TEAM_ABBREVIATION'] == home_team_abbreviation]
    away_team_row = team_df[team_df['TEAM_ABBREVIATION'] == away_team_abbreviation]

    team_df.at[home_team_row.index[0], 'Opponent'] = away_team_abbreviation
    team_df.at[away_team_row.index[0], 'Opponent'] = home_team_abbreviation
    
team_df.to_csv('C:/Users/timpr/Documents/NBA Coding Model/matchup_key.csv')


# In[2]:


#Part 2: Getting most recent team defensive stats

# Define a list of defensive play types
defensive_play_types = [
    'Isolation', 'Transition', 'Postup', 'Cut', 'Handoff', 
    'Misc', 'OffScreen', 'PRBallHandler', 'PRRollman', 'Spotup', 'OffRebound'
]

# Create an empty list to store dataframes
play_type_def_dataframes = []

# Loop through defensive play types and retrieve data
for play_type in defensive_play_types:
    play_type_def = synergyplaytypes.SynergyPlayTypes(
        play_type_nullable=play_type,
        per_mode_simple='PerGame',
        player_or_team_abbreviation='T',
        type_grouping_nullable='Defensive',
        season='2023-24'
    )
    df_play_type_def = play_type_def.get_data_frames()[0]
    play_type_def_dataframes.append(df_play_type_def)

# Concatenate all dataframes
play_type_def_combined = pd.concat(play_type_def_dataframes)

# Add a new column with team and play type information
play_type_def_combined['team_def_playtype'] = (
    play_type_def_combined['TEAM_ABBREVIATION'] + play_type_def_combined['PLAY_TYPE']
)

# Save the combined dataframe to a CSV file
play_type_def_combined.to_csv('C:/Users/timpr/Documents/NBA Coding Model/play_type_t_def.csv', index=False)


# In[3]:


#Part 3: Getting most recent team offensive stats

# Common parameters for all play types
common_params = {
    'per_mode_simple': 'PerGame',
    'player_or_team_abbreviation': 'T',
    'type_grouping_nullable': 'Offensive',
    'season': '2023-24'
}

# Define play types
play_types = [
    'Isolation', 'Transition', 'Postup', 'Cut', 'Handoff',
    'Misc', 'OffScreen', 'PRBallHandler', 'PRRollman', 'Spotup', 'OffRebound'
]

dfs = []

# Fetch data for each play type
for play_type in play_types:
    params = {'play_type_nullable': play_type, **common_params}
    play_type_data = synergyplaytypes.SynergyPlayTypes(**params).get_data_frames()[0]
    dfs.append(play_type_data)

# Concatenate data frames for all play types
play_type_t = pd.concat(dfs)
play_type_t['team_off_playtype'] = play_type_t['TEAM_ABBREVIATION'] + play_type_t['PLAY_TYPE']

# Load and merge matchup key
matchups = pd.read_csv('C:/Users/timpr/Documents/NBA Coding Model/matchup_key.csv')
play_type_t = pd.merge(play_type_t, matchups, how='inner', on='TEAM_ABBREVIATION')
play_type_t['team_def_playtype'] = play_type_t['Opponent'] + play_type_t['PLAY_TYPE']

# Load and merge defensive play type data
play_type_t_def = pd.read_csv('C:/Users/timpr/Documents/NBA Coding Model/play_type_t_def.csv')
play_type_t = pd.merge(play_type_t, play_type_t_def, how='inner', on='team_def_playtype')

# Save the final DataFrame to a CSV file
play_type_t.to_csv('C:/Users/timpr/Documents/NBA Coding Model/play_type_t_off.csv')


# In[4]:


#Part 4: Getting data for league-wide play style visualization

# Common parameters
common_params = {
    'per_mode_simple': 'PerGame',
    'player_or_team_abbreviation': 'T',
    'type_grouping_nullable': 'Offensive',
    'season': '2023-24'
}

# Define play types
play_type_names = [
    'Isolation', 'Transition', 'Postup', 'Cut', 'Handoff',
    'Misc', 'OffScreen', 'PRBallHandler', 'PRRollman', 'Spotup', 'OffRebound'
]

# Initialize a dictionary to store DataFrames
play_type_dataframes = {}

# Fetch data for each play type and store it in the dictionary
for play_type in play_type_names:
    params = {'play_type_nullable': play_type, **common_params}
    play_type_dataframes[play_type] = synergyplaytypes.SynergyPlayTypes(**params).get_data_frames()[0]

# Concatenate DataFrames for all play types
play_type_t = pd.concat(play_type_dataframes.values())
play_type_t['team_off_playtype'] = play_type_t['TEAM_ABBREVIATION'] + play_type_t['PLAY_TYPE']

# Save the DataFrame to a CSV file
play_type_t.to_csv('C:/Users/timpr/Documents/NBA Coding Model/play_type_t_viz.csv')


# In[5]:


#Part 5: Getting most recent player data

# Common parameters
common_params = {
    'per_mode_simple': 'PerGame',
    'player_or_team_abbreviation': 'P',
    'type_grouping_nullable': 'Offensive',
    'season': '2023-24'
}

# Define play types
play_type_names = [
    'Isolation', 'Transition', 'Postup', 'Cut', 'Handoff',
    'Misc', 'OffScreen', 'PRBallHandler', 'PRRollman', 'Spotup', 'OffRebound'
]

# Initialize a dictionary to store DataFrames
play_type_dataframes = {}

# Fetch data for each play type and store it in the dictionary
for play_type in play_type_names:
    params = {'play_type_nullable': play_type, **common_params}
    play_type_dataframes[play_type] = synergyplaytypes.SynergyPlayTypes(**params).get_data_frames()[0]

# Concatenate DataFrames for all play types
play_type_off = pd.concat(play_type_dataframes.values())

# Load and merge matchup key
matchups = pd.read_csv('C:/Users/timpr/Documents/NBA Coding Model/matchup_key.csv')
play_type_off = pd.merge(play_type_off, matchups, how='inner', on='TEAM_ABBREVIATION')
play_type_off['team_def_playtype'] = play_type_off['Opponent'] + play_type_off['PLAY_TYPE']
play_type_off['player_team_id'] = play_type_off['PLAYER_NAME'] + play_type_off['TEAM_ABBREVIATION']

# Load and merge defensive play type data
play_type_t_def = pd.read_csv('C:/Users/timpr/Documents/NBA Coding Model/play_type_t_def.csv')
play_type_off = pd.merge(play_type_off, play_type_t_def, how='inner', on='team_def_playtype')

# Save the DataFrame to a CSV file
play_type_off.to_csv('C:/Users/timpr/Documents/NBA Coding Model/play_type_p_off.csv')


# In[6]:


#Part 6: Getting historical player game logs

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelogs

list_players = players.get_active_players()

log_py = playergamelogs.PlayerGameLogs(season_nullable = "2022-23",date_from_nullable = "1/1/2023")
df_log_py = log_py.get_data_frames()[0]

log_cy = playergamelogs.PlayerGameLogs(season_nullable = "2023-24")
df_log_cy = log_cy.get_data_frames()[0]

player_log = pd.concat([df_log_py,df_log_cy])

player_log['PLAYER_NAME'] = player_log['PLAYER_NAME'].replace({'Cam Thomas':'Cameron Thomas'})
player_log.rename(columns={'PLAYER_NAME': 'Player'}, inplace=True)

player_log.to_csv('C:/Users/timpr/Documents/NBA Coding Model/player_logs.csv')

