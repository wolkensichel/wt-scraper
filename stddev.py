#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 16:23:41 2019

@author: Alexander Aigner
"""

import inout
import statistics
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, t

start_year = 13
end_year = 19

teams_1BL = {
        'bayern-munchen': 'Bayern München',
        '1899-hoffenheim': '1899 Hoffenheim',
        'hertha-bsc': 'Hertha BSC',
        '1-fc-nurnberg': '1. FC Nürnberg',
        'werder-bremen': 'Werder Bremen',
        'hannover-96': 'Hannover 96',
        'sc-freiburg': 'SC Freiburg',
        'eintr-frankfurt': 'Eintr. Frankfurt',
        'vfl-wolfsburg': 'VfL Wolfsburg',
        'schalke-04': 'Schalke 04',
        'fortuna-dusseldorf': 'Fortuna Düsseldorf',
        'fc-augsburg': 'FC Augsburg',
        'bor-mgladbach': "Bor. M'Gladbach",
        'bayer-leverkusen': 'Bayer Leverkusen',
        'mainz-05': 'Mainz 05',
        'vfb-stuttgart': 'VfB Stuttgart',
        'bor-dortmund': 'Bor. Dortmund',
        'rb-leipzig': 'RB Leipzig',
        'hamburger-sv': 'Hamburger SV',
        '1-fc-koln': '1. FC Köln',
        'sv-darmstadt-98': 'SV Darmstadt 98',
        'sc-paderborn': 'SC Paderborn',
        'fc-ingolstadt': 'FC Ingolstadt',
        'braunschweig': 'Braunschweig',
        'greuther-furth': 'Greuther Fürth',
        '1-fc-k-acute-lautern': '1. FC K´lautern',
        'fc-st-pauli': 'FC St. Pauli',
        'vfl-bochum': 'VfL Bochum',
        'karlsruher-sc': 'Karlsruher SC',
        'arminia-bielefeld': 'Arminia Bielefeld',
        'energie-cottbus': 'Energie Cottbus',
        'hansa-rostock': 'Hansa Rostock',
        'msv-duisburg': 'MSV Duisburg'
        }

# compile dataset from specified season years
print('-- merging files')
inputs = ['votes_s', 'votes_2BL_s']
user_stats_dict_abs = inout.mergeProContraFiles(inputs, start_year, end_year)                            


# calculate normed stats of each user per season for overall histogram
print('-- calculating normed stats of each user per season')
omit_single = True
user_stats_dict_rel = statistics.normedSeasonStats(user_stats_dict_abs, omit_single)

# calculate normed stats of each user per season for team histograms
print('-- calculating normed stats of each user per season')
omit_single = False
user_stats_dict_team_rel = statistics.normedSeasonStats(user_stats_dict_abs, omit_single)


# calculate mean number of votes per team and season
print('-- mean number of votes per team and season')
inputs = ['decisions_s', 'decisions_2BL_s']
team_dec, kt_dec, comm_dec = inout.mergeDecisionFiles(inputs, start_year, end_year)


# get histogram values for each team
side = 'pro'
hist_vals_pro = statistics.histSeasonStatsTeam(user_stats_dict_team_rel, side)
hist_vals_omit_pro = statistics.histSeasonStatsTeam(user_stats_dict_rel, side)

# merge histogram values of all teams for histogram of all teams combined
hist_vals_all_pro = []
for team_1BL in teams_1BL:
    team = teams_1BL[team_1BL]
    if team in hist_vals_omit_pro:
        hist_vals_all_pro += hist_vals_omit_pro[team]
        

# calculate mean value of combined histogram
mean = np.mean(hist_vals_all_pro)
# calculate variance
var = np.var(hist_vals_all_pro, ddof=1)
# calculate standard deviation
stdev = np.std(hist_vals_all_pro, ddof=1)
# calculate standard error
stderr = stdev / np.sqrt( len(hist_vals_all_pro) )


# standardize normal distributions
for team_1BL in teams_1BL:
    team = teams_1BL[team_1BL]
    if team in hist_vals_pro:
        hist_vals_pro[team] = [(x - mean) / stdev for x in hist_vals_pro[team]]
hist_vals_all_pro = [(x - mean) / stdev for x in hist_vals_all_pro]        


# normal distribution (target distribution)
mu = 0
sigma = 1
z1 = (-4 - mu) / sigma
z2 = ( 4 - mu) / sigma
x = np.arange(z1, z2, 0.01)
y = norm.pdf(x, mu, sigma)


# histogram for team
for team_1BL in teams_1BL:
    team = teams_1BL[team_1BL]
    if team in hist_vals_pro:
        df = len(hist_vals_pro[team]) - 1
        stdev = np.std(hist_vals_pro[team], ddof=1)
        stderr = stdev / np.sqrt( len(hist_vals_pro[team]) )
        
        print(team, ':', df, stdev, stderr)
        
        plt.figure()
        plt.hist(hist_vals_pro[team], bins='auto', density=True)
        plt.plot(x, y)
        if df > 0:
            yt = t.pdf(x, df)
            plt.plot(x, yt, color='g', ls='dashed')
        plt.title(team + ' - #values: ' + str(len(hist_vals_pro[team])))
        #plt.savefig('hist/' + team + '.png')
        #plt.close()
        plt.show()
        
# histogram of all teams combined
df = len(hist_vals_all_pro) - 1
print(df)
yt = t.pdf(x, df)

plt.figure()
#print(hist_vals_all_pro)
#hist_vals_all_pro = [x/len(hist_vals_all_pro) for x in hist_vals_all_pro]
#print(hist_vals_all_pro)
plt.hist(hist_vals_all_pro, bins='auto', density=True)
plt.plot(x, y)
plt.plot(x, yt, color='g', ls='dashed')
plt.title('all teams' + ' - #values: ' + str(len(hist_vals_all_pro)))
#plt.savefig('hist/all_teams.png')
#plt.close()
#plt.show()