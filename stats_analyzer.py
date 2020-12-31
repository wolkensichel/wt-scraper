#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 10:35:20 2019

@author: Alexander Aigner
"""

import pickle
import matplotlib.pyplot as plt
import copy
import numpy as np
import statistics

start_year = 9
end_year = 20

alpha = 0.0027 # 3*sigma

user_team_corr = False     # merge votes of fans of an involved team to one vote
omit_fan_votes = False     # remove votes of fans of an involved team
include_nonrelevant = True # include votes from nicht_relevant category

# analyze only teams that were in 1. Bundesliga in at least
# one season in specified time frame
bl1_teams = ['Bayern München',
             '1899 Hoffenheim',
             'Hertha BSC',
             '1. FC Nürnberg',
             'Werder Bremen',
             'Hannover 96',
             'SC Freiburg',
             'Eintr. Frankfurt',
             'VfL Wolfsburg',
             'Schalke 04',
             'Fortuna Düsseldorf',
             'FC Augsburg',
             "Bor. M'Gladbach",
             'Bayer Leverkusen',
             'Mainz 05',
             'VfB Stuttgart',
             'Bor. Dortmund',
             'RB Leipzig',
             'Hamburger SV',
             '1. FC Köln',
             'SV Darmstadt 98',
             'SC Paderborn',
             'FC Ingolstadt',
             'Braunschweig',
             'Greuther Fürth',
             '1. FC K´lautern',
             'FC St. Pauli',
             'VfL Bochum',
             'Karlsruher SC',
             'Arminia Bielefeld',
             'Energie Cottbus',
             'Hansa Rostock',
             'MSV Duisburg',
             '1. FC Union Berlin'
             ]

"""
kt_users = ['AbrahamLincoln', 'beyerle', 'Detlef Sparwasser', 'Ferrero', 'gaspode', 
            'hrub', 'keksjanik', 'kennet1000', 'mehrjo', 'Randy', 
            'redonyx', 'Schlusspfiff', 'Schwarzangler', 'Sinja', 'WT-Community', 
            'colognek', 'don_riddle', 'Kornex', 'schoeni', 'toopac', 
            'wölfin', '2011er', 'Dreiundnicht', 'erfolgsfan', 'Gimlin', 
            'Herthaner4ever', 'lufdbomp', 'Rüpel', 'Hagi01', 'GladbacherFohlen', 
            'Selachier', 'Stormfalco', 'JFB96', 'Adlerherz', 'Danny41', 
            'I bin I', 'Loomer', 'Mammutjäger', 'referee2023', 'SetOnFire', 
            'SmartTim98', 'Taruiezi', 'Wallmersbacher', 'eraff', 'Junior']
"""
# 2019/2020
kt_users = ['Adlerherz', 'don_riddle', 'Dreiundnicht', 'erfolgsfan', 'Ferrero', 'Gimlin', 'GladbacherFohlen', 'Hagi01', 'hrub', 'I bin I', 'JFB96', 'Junior', 'Kornex', 'lufdbomp', 'Mammutjäger', 'mehrjo', 'Randy', 'redonyx', 'Schwarzangler', 'SetOnFire', 'Stormfalco', 'Taruiezi', 'Wallmersbacher', 'WT-Community']

# create season data file names
user_lists_files = []
for i in range(end_year-start_year):
    year_var1 = str(start_year+i) if len(str(start_year+i)) == 2 else '0' + str(start_year+i)
    year_var2 = str(start_year+1+i) if len(str(start_year+1+i)) == 2 else '0' + str(start_year+1+i)
    user_lists_files.append('data_season_BL1_s' + str(year_var1) + '-' + str(year_var2) + '.pickle')
    user_lists_files.append('data_season_BL2_s' + str(year_var1) + '-' + str(year_var2) + '.pickle')

# compile file lists for kt users
users_files = {}
for file in user_lists_files:
    try:
        with open(file, 'rb') as f:
            _, users, _ = pickle.load(f)
    except:
        continue
        
    for user in users:
        if user in kt_users: 
            year = file.split('.')[0][-5:]
            if user not in users_files:
                users_files[user] = {'first_year': year, 'last_year': year, 'files': []}
            else:
                users_files[user]['last_year'] = year
            file = file.replace('data_season', 'votes')
            users_files[user]['files'].append(file)

# create votes file names
user_votes_files = []
for i in range(end_year-start_year):
    year_var1 = str(start_year+i) if len(str(start_year+i)) == 2 else '0' + str(start_year+i)
    year_var2 = str(start_year+1+i) if len(str(start_year+1+i)) == 2 else '0' + str(start_year+1+i)
    user_votes_files.append('votes_BL1_s' + str(year_var1) + '-' + str(year_var2) + '.pickle')
    user_votes_files.append('votes_BL2_s' + str(year_var1) + '-' + str(year_var2) + '.pickle')    
    
# compile data sets for kt users
print('-- reading in data from votes files')
user_stats_dict_abs = {}
for user in users_files:
    for file in users_files[user]['files']:
        with open(file, 'rb') as f:
            curr_kt_user_stats_dict_abs, curr_comm_user_stats_dict_abs = pickle.load(f)
        
        if user in curr_kt_user_stats_dict_abs:
            user_stats_abs = curr_kt_user_stats_dict_abs[user]
            if user in curr_comm_user_stats_dict_abs:
                for team in user_stats_abs:
                    if team != 'team' and team in curr_comm_user_stats_dict_abs[user]:
                        user_stats_abs[team]['relevant'][0] += curr_comm_user_stats_dict_abs[user][team]['relevant'][0]
                        user_stats_abs[team]['relevant'][1] += curr_comm_user_stats_dict_abs[user][team]['relevant'][1]
                        user_stats_abs[team]['nicht_relevant'][0] += curr_comm_user_stats_dict_abs[user][team]['nicht_relevant'][0]
                        user_stats_abs[team]['nicht_relevant'][1] += curr_comm_user_stats_dict_abs[user][team]['nicht_relevant'][1]
                        user_stats_abs[team]['nicht_relevant'][2] += curr_comm_user_stats_dict_abs[user][team]['nicht_relevant'][2]
                for team in curr_comm_user_stats_dict_abs[user]:
                    if team != 'team' and team not in user_stats_abs:
                        user_stats_abs[team] = curr_comm_user_stats_dict_abs[user][team]
        else:
            if user in curr_comm_user_stats_dict_abs:
                user_stats_abs = curr_comm_user_stats_dict_abs[user]
            else:
                print(file, user, 'not present despite vote')
                continue
            
        if user not in user_stats_dict_abs:
            user_stats_dict_abs[user] = user_stats_abs
        else:
            del user_stats_abs['team']
            for team in user_stats_abs:
                if team not in user_stats_dict_abs[user]:
                    user_stats_dict_abs[user][team] = user_stats_abs[team]
                else:
                    user_stats_dict_abs[user][team]['relevant'][0] += user_stats_abs[team]['relevant'][0]
                    user_stats_dict_abs[user][team]['relevant'][1] += user_stats_abs[team]['relevant'][1]
                    user_stats_dict_abs[user][team]['nicht_relevant'][0] += user_stats_abs[team]['nicht_relevant'][0]
                    user_stats_dict_abs[user][team]['nicht_relevant'][1] += user_stats_abs[team]['nicht_relevant'][1]
                    user_stats_dict_abs[user][team]['nicht_relevant'][2] += user_stats_abs[team]['nicht_relevant'][2]
                    

# calculate percentile for pro/contra voting pairs
print('-- calculating percentiles for user votes')
user_stats_dict_abs_perc = {}
for user in user_stats_dict_abs:
    user_stats_abs = user_stats_dict_abs[user]
    #user_unspec_votes = user_unspec_votes_dict[user]
    user_stats_dict_abs_perc[user] = {}
    
    for team in user_stats_abs:
        if team != 'team':
            cond = statistics.laplaceCondition(user_stats_abs[team], include_nonrelevant)
            if cond == True:
                percentile = statistics.votePercentileNormal(user_stats_abs[team], include_nonrelevant)
            else:
                percentile = statistics.votePercentileBinomial(user_stats_abs[team], include_nonrelevant)
            user_stats_dict_abs_perc[user][team] = percentile


# calculate normed stats for each user
print('-- calculating normed stats for each user')
user_stats_dict_rel = {}#copy.deepcopy(user_stats_dict_abs)
for user in user_stats_dict_abs:
    user_stats_abs = copy.deepcopy(user_stats_dict_abs[user])
    
    user_stats_dict_rel[user] = {}
    user_stats_dict_rel[user]['team'] = user_stats_abs['team']
    
    for team in user_stats_abs:
        if team != 'team':
            user_stats_dict_rel[user][team] = [0,0]
            if include_nonrelevant == True:
                v_all = sum(user_stats_abs[team]['relevant']) + \
                        user_stats_abs[team]['nicht_relevant'][0] + \
                        user_stats_abs[team]['nicht_relevant'][2]
                pro_v = user_stats_abs[team]['relevant'][0] + user_stats_abs[team]['nicht_relevant'][0]
                con_v = user_stats_abs[team]['relevant'][1] + user_stats_abs[team]['nicht_relevant'][2]
            else:
                v_all = sum(user_stats_abs[team]['relevant'])
                pro_v = user_stats_abs[team]['relevant'][0]
                con_v = user_stats_abs[team]['relevant'][1]
                
            if v_all != 0:
                user_stats_dict_rel[user][team][0] = pro_v / v_all
                user_stats_dict_rel[user][team][1] = con_v / v_all
            else:
                user_stats_dict_rel[user][team][0] = 0
                user_stats_dict_rel[user][team][1] = 0


# The commented section below calculates normed vote sum by adding up all votes 
# pro and contra of a team and then computing the relative percentages. The 
# method leads to higher weighting of users with more votes
"""
# calculate overall stats summing all user votes
print('-- calculating combined stats for all teams')
sum_stats_dict_abs = {}
for user in user_stats_dict_abs:
    user_stats_abs = copy.deepcopy(user_stats_dict_abs[user])
    for team in user_stats_abs:
        if team != 'team':
            if team not in sum_stats_dict_abs:
                sum_stats_dict_abs[team] = user_stats_abs[team]
            else:
                sum_stats_dict_abs[team][0] += user_stats_abs[team][0]
                sum_stats_dict_abs[team][1] += user_stats_abs[team][1]
                
                
# calculate overall normed stats combining all user votes
print('-- calculating combined normed stats for all teams')
sum_stats_dict_rel = copy.deepcopy(sum_stats_dict_abs)
for team in sum_stats_dict_rel:
    v_all = sum(sum_stats_dict_rel[team])
    if v_all != 0:
        sum_stats_dict_rel[team][0] = sum_stats_dict_rel[team][0] / v_all
        sum_stats_dict_rel[team][1] = sum_stats_dict_rel[team][1] / v_all
    else:
        sum_stats_dict_rel[team][0] = 0
        sum_stats_dict_rel[team][1] = 0
"""

# combine users that are fans of the same team to one data item to avoid 
# weighting bias in normed stats calculation
print('-- combine stats for users that are fans of same team')
user_stats_dict_rel_cmb = {}
team_user_lu = {}
for user in user_stats_dict_rel:
    user_stats_rel = copy.deepcopy(user_stats_dict_rel[user])

    fan_team = user_stats_rel['team']    
    if fan_team not in team_user_lu:
        team_user_lu[fan_team] = {}
        team_user_lu[fan_team]['user'] = user
        
        for team in user_stats_rel:
            if team != 'team':
                team_user_lu[fan_team][team] = 1
                
        user_stats_dict_rel_cmb[user] = user_stats_rel
        
    else:
        for team in user_stats_rel:
            if team != 'team':
                if team not in team_user_lu[fan_team]:
                    team_user_lu[fan_team][team] = 1
                    user_stats_dict_rel_cmb[team_user_lu[fan_team]['user']][team] = \
                                                        user_stats_rel[team]
                else:
                    team_user_lu[fan_team][team] += 1
                    user_stats_dict_rel_cmb[team_user_lu[fan_team]['user']][team][0] += \
                                                        user_stats_rel[team][0]
                    user_stats_dict_rel_cmb[team_user_lu[fan_team]['user']][team][1] += \
                                                        user_stats_rel[team][1]

for user in user_stats_dict_rel_cmb:
    user_stats_rel = user_stats_dict_rel_cmb[user]
    
    for team in user_stats_rel:
        if team != 'team':
            user_stats_rel[team][0] /= team_user_lu[user_stats_rel['team']][team]
            user_stats_rel[team][1] /= team_user_lu[user_stats_rel['team']][team]
            
    user_stats_dict_rel_cmb[user] = user_stats_rel
    

# use weight correction for voters of same teams?
if user_team_corr == False:
    user_stats_dict = copy.deepcopy(user_stats_dict_rel)
elif user_team_corr == True:
    user_stats_dict = copy.deepcopy(user_stats_dict_rel_cmb)


# calculate overall normed stats by building the arithmetic mean of all 
# relative user stats
print('-- calculating combined stats for all teams')
sum_stats_dict_rel = {}
num_users_voted = {}
for user in user_stats_dict:
    user_stats_rel = copy.deepcopy(user_stats_dict[user])
    
    for team in user_stats_rel:
        if omit_fan_votes == True:
            
            if team != 'team' and team != user_stats_rel['team']:
                if team not in sum_stats_dict_rel:
                    sum_stats_dict_rel[team] = user_stats_rel[team]
                    num_users_voted[team] = 1
                else:
                    sum_stats_dict_rel[team][0] += user_stats_rel[team][0]
                    sum_stats_dict_rel[team][1] += user_stats_rel[team][1]
                    num_users_voted[team] += 1
                    
        else:
            
            if team != 'team':
                if team not in sum_stats_dict_rel:
                    sum_stats_dict_rel[team] = user_stats_rel[team]
                    num_users_voted[team] = 1
                else:
                    sum_stats_dict_rel[team][0] += user_stats_rel[team][0]
                    sum_stats_dict_rel[team][1] += user_stats_rel[team][1]
                    num_users_voted[team] += 1
                
for team in sum_stats_dict_rel:
    sum_stats_dict_rel[team][0] /= num_users_voted[team]
    sum_stats_dict_rel[team][1] /= num_users_voted[team]


# plot results
print('-- plotting')
for user in user_stats_dict_abs:
    if user == user:
    
        user_stats_rel = user_stats_dict_rel[user]
        user_stats_abs = user_stats_dict_abs[user]
        user_percentiles = user_stats_dict_abs_perc[user]
        #user_unspec_votes = user_unspec_votes_dict[user]
        
        if user != 'WT-Community':
            own_team = user_stats_abs['team']
            
        del user_stats_rel['team']
        del user_stats_abs['team']
        
        teams = sorted(list(user_stats_rel.keys()))
        
        if 'own_team' in locals() and own_team in teams:
            teams.remove(own_team)
            teams.insert(0, own_team)
            
        # only show teams that are/were in 1. BL in specified time frame 
        rmv_list = []         
        for team in teams:
            if team not in bl1_teams:
                rmv_list.append(team)
        for team in rmv_list:
            teams.remove(team)
        
        pro_rel = []
        contra_rel = []
        pro_abs = []
        contra_abs = []
        pro_rel_all = []
        contra_rel_all = []
        
        for team in teams:
            if include_nonrelevant == True:
                pro_abs.append(user_stats_abs[team]['relevant'][0] + user_stats_abs[team]['nicht_relevant'][0])
                contra_abs.append(user_stats_abs[team]['relevant'][1] + user_stats_abs[team]['nicht_relevant'][2])
            else:
                pro_abs.append(user_stats_abs[team]['relevant'][0])
                contra_abs.append(user_stats_abs[team]['relevant'][1])
                
            pro_rel.append(user_stats_rel[team][0])
            contra_rel.append(user_stats_rel[team][1])
            
            pro_rel_all.append(sum_stats_dict_rel[team][0])
            contra_rel_all.append(sum_stats_dict_rel[team][1])
        
        contra_rel = [-x for x in contra_rel]
        contra_rel_all = [-x for x in contra_rel_all]
        
    
        #barh with correct order: top-down y axis
        plt.figure(figsize=(10,7))
        pro_bar_all = plt.barh(teams, [x*100 for x in pro_rel_all], color='navy', height=.9)
        pro_bar = plt.barh(teams, [x*100 for x in pro_rel], color='deepskyblue', height=.6)
        contra_bar_all = plt.barh(teams, [x*100 for x in contra_rel_all], color='orangered', height=.9)
        contra_bar = plt.barh(teams, [x*100 for x in contra_rel], color='orange', height=.6)
        
        ax = plt.gca()
        ax.invert_yaxis()
        ax.set_xlim([-100,100])
        ax.set_ylim([len(teams)-.4,-.6])
        ax.set_axisbelow(True)
        for label in ax.xaxis.get_ticklabels()[1::2]:
            label.set_visible(False)
        
        ylabels = ['{} ({:02}.)'.format(team, user_percentiles[team]) for team in teams]
        ax.set_yticklabels(ylabels)
        for i, team in enumerate(teams):
            # color labels if percentiles are at the edge of the normal distribution
            #if user_percentiles[team] < 0.025 or user_percentiles[team] > 0.975:
            
            # color labels if hypothesis test tells to discard Ho (user vote in distribution)
            #print(user, team, user_unspec_votes[team])
            cond = statistics.laplaceCondition(user_stats_abs[team], include_nonrelevant)
            if cond == True:
                res, bounds, marker = \
                    statistics.hypothesisTestNormal(user_stats_abs[team], include_nonrelevant, alpha)
            else:
                res, bounds, marker = \
                    statistics.hypothesisTestBinomial(user_stats_abs[team], include_nonrelevant, alpha)
            
            if res == False:
                ax.get_yticklabels()[i].set_color('orangered')
                if marker == 0:
                    plt.axvline(x= bounds['upper'], ymin=1-(i+.75)/len(teams), ymax=1-(i+.75)/len(teams), lw=1, color='crimson', marker='^', mfc='white', mew=.85, ms=6.25)
                    plt.axvline(x=-bounds['lower'], ymin=1-(i+.75)/len(teams), ymax=1-(i+.75)/len(teams), lw=1, color='crimson', marker='^', mfc='white', mew=.85, ms=6.25)
                elif marker == 1:
                    plt.axvline(x=-bounds['upper'], ymin=1-(i+.75)/len(teams), ymax=1-(i+.75)/len(teams), lw=1, color='crimson', marker='^', mfc='white', mew=.85, ms=6.25)
                    plt.axvline(x= bounds['lower'], ymin=1-(i+.75)/len(teams), ymax=1-(i+.75)/len(teams), lw=1, color='crimson', marker='^', mfc='white', mew=.85, ms=6.25)
        
        for i, bar in enumerate(pro_bar):
            if pro_abs[i] != 0:
                w_mod = 1.6 * len(str(pro_abs[i])) + .9
                plt.text(bar.get_width()-w_mod, bar.get_y()+bar.get_height()-.1, pro_abs[i], color='whitesmoke', weight='bold', fontsize=8)
        for i, bar in enumerate(contra_bar):
            if contra_abs[i] != 0:
                plt.text(bar.get_width()+.5, bar.get_y()+bar.get_height()-.1, contra_abs[i], color='whitesmoke', weight='bold', fontsize=8)
        
        if start_year+1 == end_year:
            seasons = ' (S' + users_files[user]['first_year'].replace('-','/') + ')'
        else:
            seasons = ' (S' + users_files[user]['first_year'].replace('-','/') + \
                      ' - S' + users_files[user]['last_year'].replace('-','/') + ')'
        
        plt.title('Stimmverhalten ' + user + seasons)
        plt.xlabel('Contra  (%)  Pro      ')
        ticks = [x*10-100 for x in np.arange(21)]
        labels = []
        for tick in ticks:
            if tick/10 % 2 == 0:
                labels.append(tick)
            else:
                labels.append('')
        plt.xticks(ticks, labels)
        plt.grid(True, color='lightgray')
        plt.axvspan(-60.,-40., facecolor='gainsboro', alpha=.6, zorder=0)
        plt.axvspan(40.,60., facecolor='gainsboro', alpha=.6, zorder=0)
        plt.axvspan(-.5,.5, facecolor='dimgray')
        if 'own_team' in locals() and own_team in teams:
            plt.axhspan(.525, -.6, facecolor='burlywood', alpha=.4, zorder=0)
        plt.text(102, len(teams)-.75, 'Erstellt von: celebhen / Quelle: www.wahretabelle.de', rotation=90, color='dimgray', weight='bold')
        
        plt.tight_layout()
        plt.savefig('pro_contra_stats/KT_19-20/' + user + '_pro_contra_stats_' + seasons.replace(' ','').replace('/','') + '.png')
        plt.close()
        #break
