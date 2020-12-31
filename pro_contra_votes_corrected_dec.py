#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 10:49:23 2019

@author: Alexander Aigner
"""

from urllib3 import PoolManager, ProxyManager, make_headers, util
import certifi
from bs4 import BeautifulSoup
import time # slow down request intervals
import random
import pickle

voting_results = 'votes_2BL_s19-20.pickle'
base_url = 'https://www.wahretabelle.de'
#season_url = base_url + '/?saisonId=51&spieltag=' # 1. Bundesliga
season_url = base_url + '/index/index/liga/2?saisonId=315&spieltag=' # 2. Bundesliga

# 0: named team profits
# 1: named team wronged
voting_strings = [
        ('Zu Unrecht gegebener Elfmeter für ', 0),
        ('Zu Unrecht gegebene Rote Karte für ', 1),
        ('Zu Unrecht gegebene Gelb-Rote Karte für ', 1),
        ('Reguläre Rote Karte nicht gegeben für ', 0),
        ('Reguläre Gelb-Rote Karte nicht gegeben für ', 0),
        ('Trotz Foulspiels gegebener Treffer für ', 0),
        ('Angebliches Foul, verweigertes Tor für ', 1),
        ('Nicht gegebener Elfmeter für ', 1),
        ('Abseitstor von ', 0),
        ('Tor nach unberechtigtem Freistoß für ', 0),
        ('Vermeintliches Abseits, Tor nicht gegeben für ', 1),
        ('Nicht gegebener Treffer für ', 1),
        ('nicht gegebener Freistoß - FEHLER ', 1)
        ]

teams = []
teams.append({
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
        'msv-duisburg': 'MSV Duisburg',
        '1-fc-union-berlin': '1. FC Union Berlin'
        })

teams.append({
        'sv-darmstadt-98': 'SV Darmstadt 98',
        'dynamo-dresden': 'Dynamo Dresden',
        'erzgebirge-aue': 'Erzgebirge Aue',
        'vfb-stuttgart': 'VfB Stuttgart',
        'hannover-96': 'Hannover 96',
        'greuther-furth': 'Greuther Fürth',
        'jahn-regensburg': 'Jahn Regensburg',
        'arminia-bielefeld': 'Arminia Bielefeld',
        'vfl-bochum': 'VfL Bochum',
        'wehen-wiesbaden': 'Wehen Wiesbaden',
        '1-fc-nurnberg': '1. FC Nürnberg',
        'vfl-osnabruck': 'VfL Osnabrück',
        '1-fc-heidenheim': '1. FC Heidenheim',
        'sv-sandhausen': 'SV Sandhausen',
        'karlsruher-sc': 'Karlsruher SC',
        'hamburger-sv': 'Hamburger SV',
        'fc-st-pauli': 'FC St. Pauli',
        'holstein-kiel': 'Holstein Kiel',
        'fc-ingolstadt': 'FC Ingolstadt',
        'sc-paderborn': 'SC Paderborn',
        'msv-duisburg': 'MSV Duisburg',
        '1-fc-union-berlin': '1. FC Union Berlin',
        '1-fc-koln': '1. FC Köln',
        '1-fc-magdeburg': '1. FC Magdeburg',
        '1-fc-k-acute-lautern': '1. FC K´lautern',
        'braunschweig': 'Braunschweig',
        'fc-wurzburger-kickers': 'FC Würzburger Kickers',
        'fortuna-dusseldorf': 'Fortuna Düsseldorf',
        '1860-munchen': '1860 München',
        'rb-leipzig': 'RB Leipzig',
        'sc-freiburg': 'SC Freiburg',
        'fsv-frankfurt': 'FSV Frankfurt',
        'vfr-aalen': 'VfR Aalen',
        'energie-cottbus': 'Energie Cottbus'
        })

DELAY = 1 # s
MATCHDAYS = 34

random.seed()


# request for HTML response to parse
def sendRequest(url):
    response = ''
    http = PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', url)
    http.clear()
    time.sleep(DELAY + random.uniform(1,5))

    return response


user_stats_dict = {}
comm_stats_dict = {}

# iterate through match days
for match_day in range(1,MATCHDAYS+1):
    print('Match day:', match_day)
    match_day_url = season_url + str(match_day)


    # iterate through games of match day and return match URLs
    print('-- get corrected matches')
    response = sendRequest(match_day_url)
    page = BeautifulSoup(response.data, features="html5lib")
    page = page.find('ul', attrs={'id': 'spielboxen'})
    page = page.find_all('li', attrs={'class': 'korrektur show-for-small'})
    
    corrected_matches = []
    for entry in page:
        new_match = entry.find('a').get('href')
        corrected_matches.append(new_match) 
    
    # get disputed threads of match
    print('-- get threads with corrected decisions')
    threads = []
    for match in corrected_matches:
        match_teams = match.replace('/spiel/', '')
        match_teams = match_teams.split('/')[0]
        match_teams = match_teams.split('_')
        
        if match_teams[0] in teams[0] and match_teams[1] in teams[0]:
            match_teams[0] = teams[0][match_teams[0]]
            match_teams[1] = teams[0][match_teams[1]]
        else:
            match_teams[0] = teams[1][match_teams[0]]
            match_teams[1] = teams[1][match_teams[1]]
        
        match_url = base_url + match
        response = sendRequest(match_url)
        page = BeautifulSoup(response.data, features="html5lib")
        page = page.find_all('div', attrs={'class': 'themen'})
        
        for div in page:
            if div.find('span', attrs={'class': 'thema_strittig'}):
                new_thread = (div.find('a').get('href'), match_teams)
                threads.append(new_thread)
    
    # get overall voting result of disputed thread
    print('-- get voting results')
    for thread in threads:
        thread_url = base_url + thread[0]
        response = sendRequest(thread_url)
        page = BeautifulSoup(response.data, features="html5lib")
        
        # total result of vote
        total_vote = page.find('div', attrs={'class': 'seven columns'})
        
        try:
            total_vote = total_vote.find('p', attrs={'class': 'roter-text'})
            voting_result = total_vote.text.strip()
        except:
            continue
        
        for index, result in enumerate(voting_strings):
            if result[0] in voting_result:
                pro_contra_var = result[1]
                named_team = voting_result.replace(result[0], '').strip()
                
        if 'named_team' not in locals():
            print(voting_result)
        
        
        # vote of KT members
        kt_votes = page.find('div', attrs={'id': 'teilnehmerKTModal'})
        kt_votes = kt_votes.find_all('div', attrs={'class': 'teilnehmerKTModal-stimme'})
        
        for kt_vote in kt_votes:
            vote = kt_vote.find('img', attrs={'class': 'vm mt5'}).get('title')
            try:
                user = kt_vote.find('a', attrs={'class': 's12 fb'}).text
            except:
                user = kt_vote.find('span', attrs={'class': 's12 fb'}).text
            try:
                team = kt_vote.find('span', attrs={'class': 's10 fsi'}).text.strip().replace('-Fan','')
            except:
                team = ''
            
            if user not in user_stats_dict:
                user_stats_dict[user] = {'team': team}


            if thread[1][0] == named_team:
                other_team = thread[1][1]
            else:
                other_team = thread[1][0]
                
            if (vote == 'Veto' and pro_contra_var == 0) or \
               (vote == 'richtig entschieden' and pro_contra_var == 1):
                if named_team not in user_stats_dict[user]:
                    user_stats_dict[user][named_team] = [0,1]
                else:
                    user_stats_dict[user][named_team][1] += 1
                if other_team not in user_stats_dict[user]:
                    user_stats_dict[user][other_team] = [1,0]
                else:
                    user_stats_dict[user][other_team][0] += 1
            elif (vote == 'Veto' and pro_contra_var == 1) or \
               (vote == 'richtig entschieden' and pro_contra_var == 0):
                if named_team not in user_stats_dict[user]:
                    user_stats_dict[user][named_team] = [1,0]
                else:
                    user_stats_dict[user][named_team][0] += 1
                if other_team not in user_stats_dict[user]:
                    user_stats_dict[user][other_team] = [0,1]
                else:
                    user_stats_dict[user][other_team][1] += 1
        
                    
        # vote of community members
        page = page.find('div', attrs={'id': 'teilnehmerModal'})
        
        comm_votes = page.find_all('div', attrs={'class': 'three columns ac'})
        if comm_votes == []:
            comm_votes = page.find_all('div', attrs={'class': 'four columns ac'})
        else:
            comm_votes = comm_votes[:2]
        
        for vote_class in comm_votes:
            vote = vote_class.find('th').text.strip()
            if 'keine Relevanz' in vote:
                continue
            users = vote_class.find('tbody').find_all('tr')
            
            for entry in users:
                try:
                    user = entry.find('a', attrs={'class': 's10'}).text
                except:
                    continue
                try:
                    team = entry.find('img')['title']
                except:
                    team = ''
            
                if user not in comm_stats_dict:
                    comm_stats_dict[user] = {'team': team}
    
    
                if thread[1][0] == named_team:
                    other_team = thread[1][1]
                else:
                    other_team = thread[1][0]
                    
                if (vote == 'Veto' and pro_contra_var == 0) or \
                   (vote == 'richtig entschieden' and pro_contra_var == 1):
                    if named_team not in comm_stats_dict[user]:
                        comm_stats_dict[user][named_team] = [0,1]
                    else:
                        comm_stats_dict[user][named_team][1] += 1
                    if other_team not in comm_stats_dict[user]:
                        comm_stats_dict[user][other_team] = [1,0]
                    else:
                        comm_stats_dict[user][other_team][0] += 1
                elif (vote == 'Veto' and pro_contra_var == 1) or \
                   (vote == 'richtig entschieden' and pro_contra_var == 0):
                    if named_team not in comm_stats_dict[user]:
                        comm_stats_dict[user][named_team] = [1,0]
                    else:
                        comm_stats_dict[user][named_team][0] += 1
                    if other_team not in comm_stats_dict[user]:
                        comm_stats_dict[user][other_team] = [0,1]
                    else:
                        comm_stats_dict[user][other_team][1] += 1
                        
            
with open(voting_results, 'wb') as f:
    pickle.dump([user_stats_dict, comm_stats_dict], f)
