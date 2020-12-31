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
end_year = 19

alpha = 0.0027 # 3*sigma

exclude_kt_fan = True      # exclude kt members that are fan of a involved club
exclude_wt_comm = True     # exclude community vote from decision
sum_seasons = False          # sum team stats of all seasons for plot
teams_to_compare = ['Bayern München', 'Bor. Dortmund', 'Schalke 04', 'Bayer Leverkusen', "Bor. M'Gladbach", 'RB Leipzig']

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
             'MSV Duisburg'
             ]

# kt_users = ['AbrahamLincoln', 'beyerle', 'Detlef Sparwasser', 'Ferrero', 'gaspode', 
#             'hrub', 'keksjanik', 'kennet1000', 'mehrjo', 'Randy', 
#             'redonyx', 'Schlusspfiff', 'Schwarzangler', 'Sinja', 'WT-Community', 
#             'colognek', 'don_riddle', 'Kornex', 'schoeni', 'toopac', 
#             'wölfin', '2011er', 'Dreiundnicht', 'erfolgsfan', 'Gimlin', 
#             'Herthaner4ever', 'lufdbomp', 'Rüpel', 'Hagi01', 'GladbacherFohlen', 
#             'Selachier', 'Stormfalco', 'JFB96', 'Adlerherz', 'Danny41', 
#             'I bin I', 'Loomer', 'Mammutjäger', 'referee2023', 'SetOnFire', 
#             'SmartTim98', 'Taruiezi', 'Wallmersbacher', 'eraff', 'Junior']

# create season data file names
user_lists_files = []
for i in range(end_year-start_year):
    year_var1 = str(start_year+i) if len(str(start_year+i)) == 2 else '0' + str(start_year+i)
    year_var2 = str(start_year+1+i) if len(str(start_year+1+i)) == 2 else '0' + str(start_year+1+i)
    user_lists_files.append('data_season_BL1_s' + str(year_var1) + '-' + str(year_var2) + '.pickle')
    user_lists_files.append('data_season_BL2_s' + str(year_var1) + '-' + str(year_var2) + '.pickle')

# compile stats for teams
teams_data = {}
for file in user_lists_files:
    try:
        with open(file, 'rb') as f:
            season_data, users, matchday_data = pickle.load(f)
    except:
        continue

    for matchday in matchday_data:
        for match_idx in range(len(matchday_data[matchday])):
            match = matchday_data[matchday][match_idx]

            named_team = match['vote_details']['named_team']
            other_team = match['vote_details']['other_team']

            if named_team not in teams_data:
                teams_data[named_team] = {'pro': [], 'contra': [], 'draw_irrelevant': [], 'no_kt': [], 'seasons': [], 'league': []} #'error': []
            if other_team not in teams_data:
                teams_data[other_team] = {'pro': [], 'contra': [], 'draw_irrelevant': [], 'no_kt': [], 'seasons': [], 'league': []} #'error': []

            if season_data['season_year'] not in teams_data[named_team]['seasons']:
                teams_data[named_team]['seasons'].append(str(season_data['season_year']))
                teams_data[named_team]['league'].append(season_data['league'])
                teams_data[named_team]['pro'].append(0)
                teams_data[named_team]['contra'].append(0)
                teams_data[named_team]['draw_irrelevant'].append(0)
                #teams_data[named_team]['error'].append(0)
                teams_data[named_team]['no_kt'].append(0)
            if season_data['season_year'] not in teams_data[other_team]['seasons']:
                teams_data[other_team]['seasons'].append(str(season_data['season_year']))
                teams_data[other_team]['league'].append(season_data['league'])
                teams_data[other_team]['pro'].append(0)
                teams_data[other_team]['contra'].append(0)
                teams_data[other_team]['draw_irrelevant'].append(0)
                #teams_data[other_team]['error'].append(0)
                teams_data[other_team]['no_kt'].append(0)

            if match['errors'] == 500: # not included in data set
                #teams_data[named_team]['error'][-1] += 1
                #teams_data[other_team]['error'][-1] += 1
                continue
            elif not bool(match['vote_details']['kt_votes']):
                teams_data[named_team]['no_kt'][-1] += 1
                teams_data[other_team]['no_kt'][-1] += 1
                continue

            kt_votes = match['vote_details']['kt_votes']
            if exclude_wt_comm == True:
                if 'WT-Community' in kt_votes['richtig entschieden']:
                    kt_votes['richtig entschieden'].remove('WT-Community')
                elif 'WT-Community' in kt_votes['Veto']:
                    kt_votes['Veto'].remove('WT-Community')
                #else:
                #    print('WT-Comm somewhere else', kt_votes)

            if exclude_kt_fan == True:
                for user in kt_votes['richtig entschieden']:
                    if users[user]['team'] == named_team or users[user]['team'] == other_team:
                        kt_votes['richtig entschieden'].remove(user)
                
                for user in kt_votes['Veto']:
                    if users[user]['team'] == named_team or users[user]['team'] == other_team:
                        kt_votes['Veto'].remove(user)

            if (len(kt_votes['richtig entschieden']) == 0 and len(kt_votes['Veto']) == 0) or \
                len(kt_votes['richtig entschieden']) == len(kt_votes['Veto']):
                teams_data[named_team]['draw_irrelevant'][-1] += 1
                teams_data[other_team]['draw_irrelevant'][-1] += 1
            elif len(kt_votes['richtig entschieden']) < len(kt_votes['Veto']):
                pro_contra_var = match['vote_details']['pro_contra_var']
                if pro_contra_var == 0:
                    teams_data[named_team]['contra'][-1] += 1
                    teams_data[other_team]['pro'][-1] += 1
                elif pro_contra_var == 1:
                    teams_data[named_team]['pro'][-1] += 1
                    teams_data[other_team]['contra'][-1] += 1
            elif len(kt_votes['richtig entschieden']) > len(kt_votes['Veto']):
                    teams_data[named_team]['pro'][-1] += 1
                    teams_data[other_team]['contra'][-1] += 1
            else:
                print('something weird happend', kt_votes)

#for team in teams_data:
#    print(team, teams_data[team], '\n')

teams = sorted(list(teams_data.keys()))

# remove teams not in 1. BL
rm_list = []
for team in teams:
    if team not in bl1_teams:
        rm_list.append(team)
for team in rm_list:
    teams.remove(team)

# plot results
print('-- plotting')

# plot over all seasons of teams
if sum_seasons == True:
    plt.figure(figsize=(8,6))
    ax = plt.gca()
    y = 0

    for team in teams_to_compare:
        league_indicator = sum(teams_data[team]['league']) / len(teams_data[team]['league'])
        for key in teams_data[team]:
            if key != 'league' and key != 'seasons':
                if league_indicator > 1:
                    rm_label = [rm_idx for rm_idx in range(len(teams_data[team]['league'])) if teams_data[team]['league'][rm_idx] == 2]
                    for rm_idx in sorted(rm_label, reverse=True):
                        del teams_data[team][key][rm_idx]
                teams_data[team][key] = sum(teams_data[team][key])
                
        teams_data[team]['pro_rel'] = teams_data[team]['pro'] / (teams_data[team]['pro'] + teams_data[team]['contra'] + teams_data[team]['draw_irrelevant'])
        teams_data[team]['contra_rel'] = teams_data[team]['contra'] / (teams_data[team]['pro'] + teams_data[team]['contra'] + teams_data[team]['draw_irrelevant'])
        teams_data[team]['draw_rel'] = 1 - teams_data[team]['pro_rel'] - teams_data[team]['contra_rel']

        width = 0.5  # the width of the bars
        pro_bar = plt.bar(y - width, teams_data[team]['pro'], width, color='deepskyblue', label='pro')
        contra_bar = plt.bar(y, teams_data[team]['contra'], width, color='orange', label='contra')
        draw_bar = plt.bar(y + width, teams_data[team]['draw_irrelevant'], width, color='mediumaquamarine', label='draw')
        y += 1.8

        def autolabel(bar_group):
            """Attach a text label above each bar in *bar_group*, displaying its height."""
            for bar in bar_group:
                height = bar.get_height()
                ax.annotate('{}'.format(height),
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9)


        autolabel(pro_bar)
        autolabel(contra_bar)
        autolabel(draw_bar)

    labels = teams_to_compare
    x = np.arange(len(labels))  # the label locations

    ax.set_ylabel('Szenen')
    title = 'Entscheidungen im Teamvergleich'
    if exclude_wt_comm == True:
        title += ', ohne Community-Stimme'
    if exclude_kt_fan == True:
        title += ', neutrales KT'
    ax.set_title(title)
    ax.set_xticks(x*1.8)
    ax.set_xticklabels(labels, fontsize=9)
    ax.legend(['pro', 'contra', 'draw'])

    plt.text(ax.get_xlim()[1]*1.015, 0.01*ax.get_ylim()[1], 'Erstellt von: celebhen / Quelle: www.wahretabelle.de', rotation=90, color='dimgray', weight='bold')

    plt.tight_layout()
    plt.savefig('pro_contra_stats/Teams/all_1BL_seasons/' + title + '.png')
    plt.close()

#plot season-wise decision bars
else:
    for team in teams:
        plt.figure(figsize=(8,6))
        ax = plt.gca()
        y = 0

        rm_label = []
        for idx, season in enumerate(teams_data[team]['seasons']):
            if teams_data[team]['league'][idx] == 2:
                rm_label.append(idx)
                continue
            
            width = 0.5  # the width of the bars
            pro_bar = plt.bar(y - width, teams_data[team]['pro'][idx], width, color='deepskyblue', label='pro')
            contra_bar = plt.bar(y, teams_data[team]['contra'][idx], width, color='orange', label='contra')
            draw_bar = plt.bar(y + width, teams_data[team]['draw_irrelevant'][idx], width, color='mediumaquamarine', label='draw')
            y += 1.8

            def autolabel(bar_group):
                """Attach a text label above each bar in *bar_group*, displaying its height."""
                for bar in bar_group:
                    height = bar.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=9)


            autolabel(pro_bar)
            autolabel(contra_bar)
            autolabel(draw_bar)

        labels = teams_data[team]['seasons']
        for rm_idx in sorted(rm_label, reverse=True):
            del labels[rm_idx]
        for l_idx, label in enumerate(labels):
            labels[l_idx] = label.replace('-','/')
        x = np.arange(len(labels))  # the label locations

        ax.set_ylabel('Szenen')
        ax.set_xlabel('Saison (1. BL)')
        title = 'Entscheidungen ' + team
        if exclude_wt_comm == True:
            title += ', ohne Community-Stimme'
        if exclude_kt_fan == True:
            title += ', neutrales KT'
        ax.set_title(title)
        ax.set_xticks(x*1.8)
        ax.set_xticklabels(labels, fontsize=9)
        ax.legend(['pro', 'contra', 'draw'])

        plt.text(ax.get_xlim()[1]*1.015, 0.01*ax.get_ylim()[1], 'Erstellt von: celebhen / Quelle: www.wahretabelle.de', rotation=90, color='dimgray', weight='bold')

        plt.tight_layout()
        plt.savefig('pro_contra_stats/Teams/1BL_seasons_per_team/' + title[15:] + '.png')
        plt.close()
    