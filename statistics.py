#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 12:23:15 2019

@author: Alexander Aigner
"""

import copy
import scipy.stats as st
from math import sqrt, factorial, ceil


def normedSeasonStats(stats_abs, omit_single=True, check=5):
    stats_rel = copy.deepcopy(stats_abs)
    for user in stats_rel:
        user_stats_rel = stats_rel[user]
        for team in user_stats_rel:
            if team != 'team':
                for idx, season in enumerate(user_stats_rel[team]):
                    v_all = sum(season)
                    check_val = check if omit_single == True else 0
                        
                    if v_all > check_val:
                        user_stats_rel[team][idx][0] = user_stats_rel[team][idx][0] / v_all
                        user_stats_rel[team][idx][1] = user_stats_rel[team][idx][1] / v_all
                    else:
                        user_stats_rel[team][idx][0] = None
                        user_stats_rel[team][idx][1] = None
                    
        stats_rel[user] = user_stats_rel
        
    return stats_rel


def histSeasonStatsTeam(stats_rel, side):
    hist_vals = {}
    for user in stats_rel:
        user_stats_rel = stats_rel[user]
        for team in user_stats_rel:
            if team != 'team':
                if team not in hist_vals:
                    hist_vals[team] = []
                for val_rel in user_stats_rel[team]:
                    if val_rel[0] == None:
                        continue
                    if side == 'pro':
                        hist_vals[team].append(val_rel[0])
                    elif side == 'contra':
                        hist_vals[team].append(val_rel[1])
                        
    return hist_vals


def laplaceCondition(votes, inc_nr):
    if inc_nr == True:
        n = sum(votes['relevant']) + votes['nicht_relevant'][0] + votes['nicht_relevant'][2]
    else:
        n = sum(votes['relevant'])
        
    sigma = sqrt(n*.25)
    if sigma > 3:
      condition = True
    else:
      condition = False
    return condition


def hypothesisTestNormal(votes, inc_nr, alpha):
    if inc_nr == True:
        n = sum(votes['relevant']) + votes['nicht_relevant'][0] + votes['nicht_relevant'][2]
        pro_votes = votes['relevant'][0] + votes['nicht_relevant'][0]
        con_votes = votes['relevant'][1] + votes['nicht_relevant'][2]
    else:
        n = sum(votes['relevant'])
        pro_votes = votes['relevant'][0]
        con_votes = votes['relevant'][1]
    
    mean = n*.5
    sigma = sqrt(n*.25)
    z_val_l = st.norm.ppf(alpha/2)
    z_val_u = st.norm.ppf(1-alpha/2)
    
    bounds = {}
    bounds['lower'] = mean + z_val_l*sigma
    bounds['upper'] = mean + z_val_u*sigma
    
    if bounds['lower'] > pro_votes or bounds['lower'] > con_votes:
        test_res = False
    else:
        test_res = True
        
    marker = 0 if pro_votes >= con_votes else 1
    
    bounds['lower'] *= 100/n
    bounds['upper'] *= 100/n
    
    return test_res, bounds, marker


def hypothesisTestBinomial(votes, inc_nr, alpha):
    if inc_nr == True:
        n = sum(votes['relevant']) + votes['nicht_relevant'][0] + votes['nicht_relevant'][2]
        pro_votes = votes['relevant'][0] + votes['nicht_relevant'][0]
        con_votes = votes['relevant'][1] + votes['nicht_relevant'][2]
    else:
        n = sum(votes['relevant'])
        pro_votes = votes['relevant'][0]
        con_votes = votes['relevant'][1]
    
    if n == 0:
        return True, [], 0

    if n % 2 == 0:
        limit = int(n/2)
    else:
        limit = int(1 + (n-1)/2)
    
    nPr = factorial(n)
    
    # total number of results
    num_res = 0
    for k in range(limit):
        num_res += nPr / ( factorial(k)*factorial(n-k) )
    num_res *= 2
    if n % 2 == 0:
        num_res += nPr / ( factorial(int(n/2)) )**2
    
    bounds = {}
    
    # number of results in rejection range
    num_rej = 0
    for k in range(limit):
        num_rej += nPr / ( factorial(k)*factorial(n-k) )
        # if boundaries are in histogram column
        if num_rej*2 / num_res > alpha:
            if k-1 >= pro_votes or k-1 >= con_votes:
                test_res = False
            else:
                test_res = True
            bounds['lower'] = k-1
            bounds['upper'] = n-k+1
            break
        # if boundaries are exactly on histogram column edge
        elif num_rej*2 / num_res == alpha:
            if k >= pro_votes or k >= con_votes:
                test_res = False
            else:
                test_res = True
            bounds['lower'] = k
            bounds['upper'] = n-k
            break
        
    marker = 0 if pro_votes >= con_votes else 1
    
    bounds['lower'] *= 100/n
    bounds['upper'] *= 100/n

    return test_res, bounds, marker


def votePercentileNormal(votes, inc_nr):
    #nPr = factorial(votes[0]+votes[1])
    #nCr = nPr / ( factorial(votes[0])*factorial(votes[1]) )
    # approximate binomial distribution through normal distribution
    if inc_nr == True:
        n = sum(votes['relevant']) + votes['nicht_relevant'][0] + votes['nicht_relevant'][2]
        pro_votes = votes['relevant'][0] + votes['nicht_relevant'][0]
    else:
        n = sum(votes['relevant'])
        pro_votes = votes['relevant'][0]
        
    if n == 0:
        return .5
        
    mean = n*.5
    sigma = sqrt(n*.25)
    z_val = ( pro_votes - mean ) / sigma # continuity correction -.5?
    return ceil(st.norm.cdf(z_val)*100)


def votePercentileBinomial(votes, inc_nr):
    if inc_nr == True:
        n = sum(votes['relevant']) + votes['nicht_relevant'][0] + votes['nicht_relevant'][2]
        pro_votes = votes['relevant'][0] + votes['nicht_relevant'][0]
    else:
        n = sum(votes['relevant'])
        pro_votes = votes['relevant'][0]
    
    if n == 0:
        return 50.
    
    if n % 2 == 0:
        limit = int(n/2)
    else:
        limit = int(1 + (n-1)/2)
    
    nPr = factorial(n)
    
    # total number of results
    num_res = 0
    num_perc = 0
    for k in range(limit):
        k_res = nPr / ( factorial(k)*factorial(n-k) )
        num_res += k_res
        if k == pro_votes or k == n-pro_votes:
            num_perc += k_res/2
            #k_range = k_res/2
        elif (k < pro_votes and pro_votes <= n/2) or \
             (k < n-pro_votes and pro_votes >= n/2):
            num_perc += k_res
            
    num_res *= 2
    if n % 2 == 0:
        k_res = nPr / ( factorial(int(n/2)) )**2
        num_res += k_res
        if pro_votes == int(n/2):
            num_perc += k_res/2
            #k_range = k_res/2
    
    if pro_votes > n/2:
        perc_val = (num_res - num_perc) / num_res # num_res - num_perc +/- k_range for upper/lower bnd
    else:
        perc_val = (num_perc) / num_res # num_res - num_perc +/- k_range for upper/lower bnd
        
    return ceil(100*perc_val)