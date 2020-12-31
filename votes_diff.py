#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 19:40:24 2019

@author: wolkensichel
"""

import pickle

file1 = 'old_votes_BL1_s12-13.pickle'
file2 = 'votes_BL1_s12-13.pickle'

with open(file1, 'rb') as f:
    _, user_d = pickle.load(f)
    
with open(file2, 'rb') as f:
    _, user_v = pickle.load(f)
    
cnt_corr = 0
cnt_incorr = 0
for user in user_d:
    if user not in user_v:
        print('user not in user_v:', user)
        continue
    for team in user_d[user]:
        if team != 'team' and team in user_v[user]:
            if user_d[user][team]['relevant'][0] == user_v[user][team]['relevant'][0] and \
                user_d[user][team]['relevant'][1] == user_v[user][team]['relevant'][1] and \
                user_d[user][team]['nicht_relevant'][0] == user_v[user][team]['nicht_relevant'][0] and \
                user_d[user][team]['nicht_relevant'][1] == user_v[user][team]['nicht_relevant'][1] and \
                user_d[user][team]['nicht_relevant'][2] == user_v[user][team]['nicht_relevant'][2]:
                cnt_corr += 1
            else:
                print(user, team, user_d[user][team], user_v[user][team])
                cnt_incorr += 1
        else:
            if team != 'team':
                print('team not in user_v:', team)
          
cnt_all = cnt_corr + cnt_incorr
print('corr:', cnt_corr/cnt_all, ', incorr:', cnt_incorr/cnt_all)

for user in user_v:
    if user not in user_d:
        print('user not in user_d:', user)
        continue
    for team in user_v[user]:
        if team != 'team' and team not in user_d[user]:
            print('team not in user_d:', user, '\t', team)