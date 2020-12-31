#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 14:46:15 2019

@author: wolkensichel
"""

import pickle
import os

#userlist = {('WT-Community',1),
#            ('mehrjo',0),
#            ('Dreiundnicht',0),
#            ('lufdbomp',0),
#            ('wölfin',0),
#            ('Schwarzangler',2),
#            ('Hagi01',0),
#            ('erfolgsfan',0),
#            ('GladbacherFohlen',0),
#            ('toopac',1),
#            ('Gimlin',0),
#            ('don_riddle',0)
#        }

#file1 = 'decisions_s17-18.pickle'
#file2 = 'votes_BL1_s12-13.pickle'
file3 = 'data_season_BL1_s18-19.pickle'

#with open(file1, 'rb') as f:
#    team_d, kt_d, user_d = pickle.load(f)
    
with open(file3, 'rb') as f:
    season_data, users, matchday_data = pickle.load(f)
#    kt, users = pickle.load(f)

#for user in kt_d:
#    for team in kt_d[user]:
#        if team != 'team':
#            print(user, team, kt_d[user][team], kt_v[user][team], \
#                  kt_d[user][team]-sum(kt_v[user][team]['relevant'])-sum(kt_v[user][team]['nicht_relevant']))

#print(season_data)
#print('\n\n\n\n\n')
print(matchday_data)
#print('\n\n\n\n\n')
#print(matchday_data)

#for user in kt_v:
#    for entry in userlist:
#        if user == entry[0]:
#            for team in kt_v[user]:
#                if team == '1. FC Köln' and entry[1] == 1:
#                    kt_v[user][team]['relevant'][0] -= 1
#                    kt_v[user][team]['relevant'][1] += 1
#                elif team == '1. FC Köln' and entry[1] == 0:
#                    kt_v[user][team]['relevant'][0] += 1
#                    kt_v[user][team]['relevant'][1] -= 1
#                elif team == 'Schalke 04' and entry[1] == 1:
#                    kt_v[user][team]['relevant'][0] += 1
#                    kt_v[user][team]['relevant'][1] -= 1
#                elif team == 'Schalke 04' and entry[1] == 0:
#                    kt_v[user][team]['relevant'][0] -= 1
#                    kt_v[user][team]['relevant'][1] += 1
#
#for user in user_v:
#    for entry in userlist:
#        if user == entry[0]:
#            for team in user_v[user]:
#                if team == '1. FC Köln' and entry[1] == 1:
#                    user_v[user][team]['relevant'][0] -= 1
#                    user_v[user][team]['relevant'][1] += 1
#                elif team == '1. FC Köln' and entry[1] == 0:
#                    user_v[user][team]['relevant'][0] += 1
#                    user_v[user][team]['relevant'][1] -= 1
#                elif team == 'Schalke 04' and entry[1] == 1:
#                    user_v[user][team]['relevant'][0] += 1
#                    user_v[user][team]['relevant'][1] -= 1
#                elif team == 'Schalke 04' and entry[1] == 0:
#                    user_v[user][team]['relevant'][0] -= 1
#                    user_v[user][team]['relevant'][1] += 1
#                    
#if os.path.isfile(file2):
#    os.remove(file2)
#        
#with open(file2, 'wb') as f:
#    pickle.dump([kt_v, user_v], f)

#cnt = 0
#for team in teams:
#    cnt += int(teams[team]['num_votes'])
#    
#print(cnt/2)
