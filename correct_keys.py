#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 20:04:04 2019

@author: Alexander Aigner
"""

import pickle

file = 'user_votes_s17-18.pickle'
wrong_team_name = " Schalke 04"

with open(file, 'rb') as f:
    user_stats_dict_abs = pickle.load(f)

#temp_dict = {}
#temp_dict['Hannover 96'] = user_stats_dict_abs[' Hannover 96']
#user_stats_dict_abs.pop(' Hannover 96')

for user in user_stats_dict_abs:
    user_stats_abs = user_stats_dict_abs[user]
    if wrong_team_name in user_stats_abs:
        user_stats_abs.pop(wrong_team_name)
        user_stats_abs[wrong_team_name.strip()][1] += 1

with open(file, 'wb') as f:
    pickle.dump(user_stats_dict_abs, f)   