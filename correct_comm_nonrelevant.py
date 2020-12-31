#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:32:59 2019

@author: wolkensichel
"""

import pickle

file1 = 'votes_2BL_s18-19.pickle'
file2 = 'votes_2BL_s18-19_2.pickle'

with open(file1, 'rb') as f:
    kt, users = pickle.load(f)
    
for user in users:
    for team in users[user]:
        if team != 'team':
            users[user][team]['nicht_relevant'][1] = \
                users[user][team]['nicht_relevant'][0] + users[user][team]['nicht_relevant'][2]
            users[user][team]['nicht_relevant'][0] = 0
            users[user][team]['nicht_relevant'][2] = 0
            
with open(file2, 'wb') as f:
    pickle.dump([kt, users], f)