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
import webbrowser
import os
import interventionlist as ilst

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
        ('nicht gegebener Freistoß - FEHLER ', 1),
        ('Kein Tor trotz überschrittener Linie für ', 1),
        ('Zu Unrecht gegebener Treffer ', 0),
        ('Tor trotz nicht überschrittener Linie für ', 0)
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

DELAY = 0 # s
MATCHDAYS = 34
base_url = 'https://www.wahretabelle.de'

random.seed()


season_ids = {}
season_ids['BL1'] = [
        (314,'19-20'),
#        (311,'18-19'),
#        (307,'17-18'),
#        (302,'16-17'),
#        (205,'15-16'),
#        (202,'14-15'),
#        (93,'13-14'),
#        (89,'12-13'),
#        (86,'11-12'),
#        (83,'10-11'),
#        (80,'09-10')
        ]
season_ids['BL2'] = [
        (315,'19-20'),
#        (312,'18-19'),
#        (308,'17-18'),
#        (303,'16-17'),
#        (206,'15-16'),
#        (203,'14-15'),
#        (97,'13-14')
        ]


# request for HTML response to parse
def sendRequest(url):
    response = ''
    http = PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', url)
    http.clear()
    time.sleep(DELAY + random.uniform(1,5))

    return response


def activeInterventionDialog(url, teams):
    webbrowser.open(url)
    print('>>', url)
    
    while True:
        named_team = input('>> Team profiting from correct vote: ')
        if named_team in teams:
            break
        else:
            continue
    
    if named_team == teams[0]:
        other_team = teams[1]
    else:
        other_team = teams[0]
        
    return named_team, other_team


# special interventions
def assignFromInterventionList(teams, season_id, match_day, intervention_cnt):
    if match_day == ilst.interventions[str(season_id)][intervention_cnt][1]:
        named_team = ilst.interventions[str(season_id)][intervention_cnt][0]
        print('>> successful intervention:', season_id, match_day, teams)
    else:
        named_team = ''
        
    if named_team not in teams:
        while True:
            print('>> Season', season_id, '- Counter', intervention_cnt, '- Matchday', match_day, teams)
            named_team = input('>> Team profiting from correct vote: ')
            if named_team in teams:
                break
            else:
                continue
    
    if named_team == teams[0]:
        other_team = teams[1]
    else:
        other_team = teams[0]
        
    intervention_cnt += 1
        
    return named_team, other_team, intervention_cnt


for id_pos in range(len(season_ids['BL2'])):
    season_id = season_ids['BL2'][id_pos][0]
    season_year = season_ids['BL2'][id_pos][1]
    voting_results = 'votes_BL2_s' + season_year + '.pickle'
    #season_url = base_url + '/index/index/liga/1?saisonId=' + str(season_id) + '&spieltag=' # 1. Bundesliga
    season_url = base_url + '/index/index/liga/2?saisonId=' + str(season_id) + '&spieltag=' # 2. Bundesliga

    user_stats_dict = {}
    comm_stats_dict = {}
    classes = ['corrected', 'disputed']
    sum_threads = 0
    intervention_cnt = 0
    
    # iterate through match days
    for match_day in range(1,MATCHDAYS+1):
        print('Match day:', match_day)
        match_day_url = season_url + str(match_day)
    
    
        # iterate through games of match day and return match URLs
        print('-- get corrected and disputed matches')
        response = sendRequest(match_day_url)
        page = BeautifulSoup(response.data, features="html5lib")
        page = page.find('ul', attrs={'id': 'spielboxen'})
        
        matches = []
        for cl in classes:
            if cl == 'corrected':
                p = page.find_all('li', attrs={'class': 'korrektur show-for-small'})
            elif cl == 'disputed':
                p = page.find_all('li', attrs={'class': 'strittig show-for-small'})
            
            for entry in p:
                new_match = entry.find('a').get('href')
                matches.append(new_match)
        
        
        # get disputed threads of match
        print('-- get threads with decisions in corrected and disputed matches')
        threads = [] 
        for match in matches:
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
                    
        sum_threads += len(threads)
        
        # get overall voting result of disputed thread
        print('-- get voting results from', str(len(threads)), 'threads')
        for thread in threads:
            thread_url = base_url + thread[0] + '&page=1'
            response = sendRequest(thread_url)
            page = BeautifulSoup(response.data, features="html5lib")
            
            error_check = page.find('div', attrs={'class': 'nine columns'})
            try:
                error_check = error_check.find('h1').text
                print(error_check)
                if error_check == 'Error 500':
                    continue
            except:
                pass
            
            # total result of vote
            kt_team = True
            total_vote = page.find('div', attrs={'class': 'seven columns'})
            if total_vote == None:
                cl = 'disputed'
                kt_team = False
            else:
                voting_result = total_vote.find('p', attrs={'class': 'roter-text'})
                if voting_result != None:
                    cl = 'corrected'
                    voting_result = voting_result.text.strip()
                else:
                    voting_result = total_vote.find('p', attrs={'class': 'gruener-text'})
                    if voting_result != None:
                        cl = 'disputed'
                    else:
                        voting_result = total_vote.find('p', attrs={'class': 'neutraler-text'})
                        cl = 'neutral'
            
            if cl == 'corrected':
                # find benefiting team by parsing overall voting result string
                for index, result in enumerate(voting_strings):
                    if result[0] in voting_result:
                        pro_contra_var = result[1]
                        named_team = voting_result.replace(result[0], '').strip()
                        break
                    if index == len(voting_strings)-1:
                        print('Missing result string:', voting_result)
                        
                if 'named_team' not in locals():
                    print(voting_result)
                    
                if thread[1][0] == named_team:
                    other_team = thread[1][1]
                else:
                    other_team = thread[1][0]
            
            elif cl == 'disputed' or cl == 'neutral':
                # try to find benefiting team by looking at final result vs. corrected result
                # and voting result, if all corrections concern only one of the teams
                match = page.find('li', attrs={'class': 'aktiv korrektur show-for-small'})
                if match == None:
                    rel_veto = 0
                else:
                    corrections = match.find('h4').text
                    num_corrections = int(corrections.split(' ')[0])
                    
                    vote_box = None
                    page_cnt = 1
                    while vote_box == None:
                        vote_box = page.find('div', attrs={'class': 'abstimmung-forum-box'})
                        if vote_box == None:
                            page_cnt += 1
                            thread_url = thread_url.split('page=')[0]
                            thread_url += 'page=' + str(page_cnt)
                            response = sendRequest(thread_url)
                            page = BeautifulSoup(response.data, features="html5lib")
                        else:
                            break
    
                    vote_box = vote_box.find('div', attrs={'class': 'row'})
                    rel_veto = vote_box.text.split('Veto:')[1].strip()
                    rel_veto = float(rel_veto.split('%')[0].strip().replace(',','.'))
                    
                    official_res = match.find('p', attrs={'class': 'offizielles_ergebnis'}).text
                    if official_res == '':
                        rel_veto = 0
                    else:
                        official_res = official_res.split(' : ')
                    corrected_res = match.find('p', attrs={'class': 'wahres_ergebnis'}).text
                    corrected_res = corrected_res.split(' : ')
                
                if rel_veto > 50 and (abs(int(official_res[0]) - int(corrected_res[0])) == num_corrections or \
                    abs(int(official_res[1]) - int(corrected_res[1])) == num_corrections):
                    pro_contra_var = 0
                    if int(official_res[0]) > int(corrected_res[0]):
                        named_team = thread[1][0]
                        other_team = thread[1][1]
                    elif int(official_res[1]) > int(corrected_res[1]):
                        named_team = thread[1][1]
                        other_team = thread[1][0]
                    elif int(official_res[0]) < int(corrected_res[0]):
                        named_team = thread[1][1]
                        other_team = thread[1][0]
                    elif int(official_res[1]) < int(corrected_res[1]):
                        named_team = thread[1][0]
                        other_team = thread[1][1]
                else:
                    # if more than one correction find benefiting team by looking at community user votes
                    num_users_team = {}
                    for team in thread[1]:
                        num_users_team[team] = {}
                        num_users_team[team]['correct'] = 0
                        num_users_team[team]['veto'] = 0
                        votes = page.find('div', attrs={'id': 'teilnehmerModal'})                    
                        votes = votes.find_all('div', attrs={'class': 'three columns ac'})
        
                        if votes == []:
                            votes = page.find_all('div', attrs={'class': 'four columns ac'})
                        else:
                            votes = votes[:2]
                            
                        for vote_class in votes:
                            vote = vote_class.find('th').text.strip()
                            
                            if 'keine Relevanz' in vote:
                                continue
                            elif 'Veto' in vote:
                                dec = 'veto'
                            elif 'richtig entschieden' in vote:
                                dec = 'correct'
                                
                            users = vote_class.find('tbody').find_all('tr')
                    
                            for entry in users:
                                try:
                                    user_team = entry.find('img')['title']
                                except:
                                    continue
                                
                                if user_team == team:
                                    num_users_team[team][dec] += 1
                    
                    if (num_users_team[thread[1][0]]['correct'] + num_users_team[thread[1][0]]['veto'] != 0) and \
                        (num_users_team[thread[1][1]]['correct'] + num_users_team[thread[1][1]]['veto'] != 0):
                        if (num_users_team[thread[1][0]]['correct'] > num_users_team[thread[1][0]]['veto'] and \
                            num_users_team[thread[1][1]]['correct'] < num_users_team[thread[1][1]]['veto']) or \
                            (num_users_team[thread[1][0]]['correct'] == num_users_team[thread[1][0]]['veto'] and \
                            num_users_team[thread[1][1]]['correct'] < num_users_team[thread[1][1]]['veto']) or \
                            (num_users_team[thread[1][0]]['correct'] > num_users_team[thread[1][0]]['veto'] and \
                            num_users_team[thread[1][1]]['correct'] == num_users_team[thread[1][1]]['veto']):
                            pro_contra_var = 0
                            named_team = thread[1][0]
                            other_team = thread[1][1]
                        elif (num_users_team[thread[1][0]]['correct'] < num_users_team[thread[1][0]]['veto'] and \
                            num_users_team[thread[1][1]]['correct'] > num_users_team[thread[1][1]]['veto']) or \
                            (num_users_team[thread[1][0]]['correct'] == num_users_team[thread[1][0]]['veto'] and \
                            num_users_team[thread[1][1]]['correct'] > num_users_team[thread[1][1]]['veto']) or \
                            (num_users_team[thread[1][0]]['correct'] < num_users_team[thread[1][0]]['veto'] and \
                            num_users_team[thread[1][1]]['correct'] == num_users_team[thread[1][1]]['veto']):
                            pro_contra_var = 0
                            named_team = thread[1][1]
                            other_team = thread[1][0]
                        else:
                            pro_contra_var = 0
                            #named_team, other_team = activeInterventionDialog(thread_url, thread[1])
                            named_team, other_team, intervention_cnt = \
                                assignFromInterventionList(thread[1], season_id, match_day, intervention_cnt)
                    else:
                        pro_contra_var = 0
                        #named_team, other_team = activeInterventionDialog(thread_url, thread[1])
                        named_team, other_team, intervention_cnt = \
                            assignFromInterventionList(thread[1], season_id, match_day, intervention_cnt)
                
            
            # vote of KT members
            print('-- [', thread[1][0], '-', thread[1][1], '] parsing KT team votes')
            if kt_team == True:
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
                    
                    for team in thread[1]:
                        if team not in user_stats_dict[user]:
                            user_stats_dict[user][team] = {}
                            user_stats_dict[user][team]['relevant'] = [0,0]
                            user_stats_dict[user][team]['nicht_relevant'] = [0,0,0]
                        
                    
                    if (vote == 'Veto' and pro_contra_var == 0) or \
                        (vote == 'richtig entschieden' and pro_contra_var == 1):
                        user_stats_dict[user][named_team]['relevant'][1] += 1
                        user_stats_dict[user][other_team]['relevant'][0] += 1
                    elif (vote == 'Veto' and pro_contra_var == 1) or \
                        (vote == 'richtig entschieden' and pro_contra_var == 0):
                        user_stats_dict[user][named_team]['relevant'][0] += 1
                        user_stats_dict[user][other_team]['relevant'][1] += 1
                    elif vote == 'richtig, keine Relevanz':
                        user_stats_dict[user][named_team]['nicht_relevant'][0] += 1
                        user_stats_dict[user][other_team]['nicht_relevant'][2] += 1
                    elif vote == 'Veto, keine Relevanz':
                        user_stats_dict[user][named_team]['nicht_relevant'][2] += 1
                        user_stats_dict[user][other_team]['nicht_relevant'][0] += 1      
                    elif vote == 'nicht zu beurteilen' or vote == 'keine Relevanz/unentschieden':
                        user_stats_dict[user][named_team]['nicht_relevant'][1] += 1
                        user_stats_dict[user][other_team]['nicht_relevant'][1] += 1 
                    else:
                        print('Unexpected string in KT votes:', vote)
            
                        
            # vote of community members
            print('-- [', thread[1][0], '-', thread[1][1], '] parsing community user votes')
            page = page.find('div', attrs={'id': 'teilnehmerModal'})
            
            comm_votes = page.find_all('div', attrs={'class': 'three columns ac'})
            if comm_votes == []:
                comm_votes = page.find_all('div', attrs={'class': 'four columns ac'})
            else:
                comm_votes = comm_votes[:2]
            
            for vote_class in comm_votes:
                vote = vote_class.find('th').text.strip()
                
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
                    
                    for team in thread[1]:
                        if team not in comm_stats_dict[user]:
                            comm_stats_dict[user][team] = {}
                            comm_stats_dict[user][team]['relevant'] = [0,0]
                            comm_stats_dict[user][team]['nicht_relevant'] = [0,0,0]
                    
                    
                    if (vote == 'Veto' and pro_contra_var == 0) or \
                        (vote == 'richtig entschieden' and pro_contra_var == 1):
                        comm_stats_dict[user][named_team]['relevant'][1] += 1
                        comm_stats_dict[user][other_team]['relevant'][0] += 1
                    elif (vote == 'Veto' and pro_contra_var == 1) or \
                        (vote == 'richtig entschieden' and pro_contra_var == 0):
                        comm_stats_dict[user][named_team]['relevant'][0] += 1
                        comm_stats_dict[user][other_team]['relevant'][1] += 1
                    elif 'keine Relevanz' in vote:
                        comm_stats_dict[user][named_team]['nicht_relevant'][1] += 1
                        comm_stats_dict[user][other_team]['nicht_relevant'][1] += 1
                    else:
                        print('Unexpected string in Community votes:', vote)
                        
        print('-- adding matchday to file')
        if os.path.isfile(voting_results):
            os.remove(voting_results)
        with open(voting_results, 'wb') as f:
            pickle.dump([user_stats_dict, comm_stats_dict], f)
        
    print('#threads:', sum_threads)
