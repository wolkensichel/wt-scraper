#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 13:11:47 2019

@author: Alexander Aigner
"""

import pickle

season = '09-10'

file_kt = 'user_votes_s' + season + '.pickle'
file_comm = 'comm_votes_s' + season + '.pickle'
file = 'votes_s' + season + '.pickle'

with open(file_kt, 'rb') as f:
    user_stats_dict_abs = pickle.load(f)
    
with open(file_comm, 'rb') as f:
    comm_stats_dict_abs = pickle.load(f)
    
with open(file, 'wb') as f:
    pickle.dump([user_stats_dict_abs, comm_stats_dict_abs], f)