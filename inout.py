#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 11:57:39 2019

@author: Alexander Aigner
"""

import pickle


def mergeProContraStats(stats_abs, stats):
    for user in stats_abs:
        user_stats_abs = stats_abs[user]
        
        if user not in stats:
            stats[user] = {}
            for team in user_stats_abs:
                if team == 'team':
                    stats[user][team] = user_stats_abs[team]
                else:
                    stats[user][team] = []
                    stats[user][team].append(user_stats_abs[team])
        else:
            for team in user_stats_abs:
                if team != 'team':
                    if team not in stats[user]:
                        stats[user][team] = []
                        stats[user][team].append(user_stats_abs[team])
                    else:
                        stats[user][team].append(user_stats_abs[team])
                        
    return stats


def mergeProContraFiles(inputs, start_year, end_year):
    stats = {}
    for i in range(end_year-start_year):
        year_var1 = str(start_year+i) if len(str(start_year+i)) == 2 else '0' + str(start_year+i)
        year_var2 = str(start_year+1+i) if len(str(start_year+1+i)) == 2 else '0' + str(start_year+1+i)
        
        input_files = []
        for file_name in inputs:
            input_files.append(file_name + str(year_var1) + '-' + str(year_var2) + '.pickle')
        
        for file in input_files:
            try:
                with open(file, 'rb') as f:
                    kt_stats_abs, comm_stats_abs = pickle.load(f)
            except:
                continue
            
            stats = mergeProContraStats(kt_stats_abs, stats)

    return stats


def mergeTeamStats(stats_abs, stats):
    for team in stats_abs:
        team_stats_abs = stats_abs[team]
        
        if team not in stats:
            stats[team] = team_stats_abs
        else:
            for idx, val in enumerate(team_stats_abs['all_votes']):
                stats[team]['all_votes'][idx] += val
            for idx, val in enumerate(team_stats_abs['pro_contra']):
                stats[team]['pro_contra'][idx] += val
    
    return stats


def mergeUserStats(stats_abs, stats):
    for user in stats_abs:
        user_stats_abs = stats_abs[user]
        
        if user not in stats:
            stats[user] = user_stats_abs
        else:
            for team in user_stats_abs:
                if team != 'team':
                    if team not in stats[user]:
                        stats[user][team] = user_stats_abs[team]
                    else:
                        stats[user][team] += user_stats_abs[team]
                    
    return stats


def mergeDecisionFiles(inputs, start_year, end_year):
    team_stats = {}
    kt_stats = {}
    comm_stats = {}
    for i in range(end_year-start_year):
        year_var1 = str(start_year+i) if len(str(start_year+i)) == 2 else '0' + str(start_year+i)
        year_var2 = str(start_year+1+i) if len(str(start_year+1+i)) == 2 else '0' + str(start_year+1+i)
        
        input_files = []
        for file_name in inputs:
            input_files.append(file_name + str(year_var1) + '-' + str(year_var2) + '.pickle')
            
        for file in input_files:
            try:
                with open(file, 'rb') as f:
                    team_stats_abs, kt_stats_abs, comm_stats_abs = pickle.load(f)
            except:
                continue
            
            team_stats = mergeTeamStats(team_stats_abs, team_stats)
            kt_stats = mergeUserStats(kt_stats_abs, kt_stats)
            comm_stats = mergeUserStats(comm_stats_abs, comm_stats)
            
    return team_stats, kt_stats, comm_stats