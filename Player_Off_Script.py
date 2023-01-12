#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
import pandas as pd
import nba_api as nba
from pandas import Series, DataFrame


# In[7]:


from nba_api.stats.endpoints import synergyplaytypes
iso = synergyplaytypes.SynergyPlayTypes(play_type_nullable='Isolation',per_mode_simple='PerGame',player_or_team_abbreviation='P',type_grouping_nullable='Offensive',season='2022-23')
transition = synergyplaytypes.SynergyPlayTypes(play_type_nullable='Transition',per_mode_simple='PerGame',player_or_team_abbreviation='P',type_grouping_nullable='Offensive',season='2022-23')
postup = synergyplaytypes.SynergyPlayTypes(play_type_nullable='Postup',per_mode_simple='PerGame',player_or_team_abbreviation='P',type_grouping_nullable='Offensive',season='2022-23')
cut = synergyplaytypes.SynergyPlayTypes(play_type_nullable='Cut',per_mode_simple='PerGame',player_or_team_abbreviation='P',type_grouping_nullable='Offensive',season='2022-23')
handoff = synergyplaytypes.SynergyPlayTypes(play_type_nullable='Handoff',per_mode_simple='PerGame',player_or_team_abbreviation='P',type_grouping_nullable='Offensive',season='2022-23')
misc = synergyplaytypes.SynergyPlayTypes(play_type_nullable='Misc',per_mode_simple='PerGame',player_or_team_abbreviation='P',type_grouping_nullable='Offensive',season='2022-23')
off_screen = synergyplaytypes.SynergyPlayTypes(play_type_nullable='OffScreen',per_mode_simple='PerGame',player_or_team_abbreviation='P',type_grouping_nullable='Offensive',season='2022-23')
pnrhandler = synergyplaytypes.SynergyPlayTypes(play_type_nullable='PRBallHandler',per_mode_simple='PerGame',player_or_team_abbreviation='P',type_grouping_nullable='Offensive',season='2022-23')
pnrroll = synergyplaytypes.SynergyPlayTypes(play_type_nullable='PRRollman',per_mode_simple='PerGame',player_or_team_abbreviation='P',type_grouping_nullable='Offensive',season='2022-23')
spotup = synergyplaytypes.SynergyPlayTypes(play_type_nullable='Spotup',per_mode_simple='PerGame',player_or_team_abbreviation='P',type_grouping_nullable='Offensive',season='2022-23')
putback = synergyplaytypes.SynergyPlayTypes(play_type_nullable='OffRebound',per_mode_simple='PerGame',player_or_team_abbreviation='P',type_grouping_nullable='Offensive',season='2022-23')


# In[8]:


df_iso = iso.get_data_frames()[0]
df_transition = transition.get_data_frames()[0]
df_postup = postup.get_data_frames()[0]
df_cut = cut.get_data_frames()[0]
df_handoff = handoff.get_data_frames()[0]
df_misc = misc.get_data_frames()[0]
df_off_screen = off_screen.get_data_frames()[0]
df_pnrhandler = pnrhandler.get_data_frames()[0]
df_pnrroll = pnrroll.get_data_frames()[0]
df_spotup = spotup.get_data_frames()[0]
df_putback = putback.get_data_frames()[0]


# In[9]:


play_type_off = [df_iso, df_transition, df_postup, df_cut, df_handoff, df_misc, df_off_screen, df_pnrhandler, df_pnrroll, df_spotup, df_putback]
play_type_off = pd.concat(play_type_off)


# In[10]:


play_type_off.to_csv('C:/Users/TimothyPrier/Documents/Practice/play_type_p_off.csv')

