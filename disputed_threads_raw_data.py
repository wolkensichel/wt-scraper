#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 10:34:31 2019

@author: Alexander Aigner
"""

from urllib3 import PoolManager, ProxyManager, make_headers, util
import certifi
from bs4 import BeautifulSoup
import time # slow down request intervals
import random
import pickle
#import webbrowser
#import os
import interventionlist as ilst

DELAY = 1 # s
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

match_classes = ['corrected', 'disputed']

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



# request for HTML response to parse
def sendRequest(url):
    response = ''
    http = PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', url)
    http.clear()
    time.sleep(DELAY + random.uniform(1,5))

    return response


def decisionDialog(teams, season_id, match_day, intervention_cnt, thread_url):
    while True:
        print(thread_url)
        print('>> Season', season_id, '- Counter', intervention_cnt, '- Matchday', match_day, teams)
        named_team = input('>> Team profiting from correct vote: ')
        if named_team in teams:
            return named_team
            

# special interventions
def assignFromInterventionList(teams, season_id, match_day, intervention_cnt, thread_url):
    if len(ilst.interventions[str(season_id)]) == 0:
        named_team = decisionDialog(teams, season_id, match_day, intervention_cnt, thread_url)
    else:
        if match_day == ilst.interventions[str(season_id)][intervention_cnt][1]:
            named_team = ilst.interventions[str(season_id)][intervention_cnt][0]
            print('>> successful intervention:', season_id, match_day, teams)
        else:
            named_team = ''
        
        if named_team not in teams:
            named_team = decisionDialog(teams, season_id, match_day, intervention_cnt, thread_url)

    if named_team == teams[0]:
        other_team = teams[1]
    else:
        other_team = teams[0]
            
    intervention_cnt += 1
        
    return named_team, other_team, intervention_cnt


# iterate through games of match day and return match URLs
def getRelevantMatches(matchday_url):
    print('-- get corrected and disputed matches')
    response = sendRequest(matchday_url)
    page = BeautifulSoup(response.data, features="html5lib")
    page = page.find('ul', attrs={'id': 'spielboxen'})
    
    matches = []
    for mc in match_classes:
        if mc == 'corrected':
            p = page.find_all('li', attrs={'class': 'korrektur show-for-small'})
        elif mc == 'disputed':
            p = page.find_all('li', attrs={'class': 'strittig show-for-small'})
        
        for entry in p:
            new_match = entry.find('a').get('href')
            matches.append(new_match)
            
    return matches


# get disputed threads of match
def getDisputedThreads(matches):
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
                
    return threads


# get overall voting result of disputed thread
def getVotingResult(page, thread):
    kt_team = True
    total_vote = page.find('div', attrs={'class': 'seven columns'})
    if total_vote == None:
        cl = 'no_kt_vote'
        kt_team = False
        voting_result = ''
    else:
        voting_result = total_vote.find('p', attrs={'class': 'roter-text'})
        if voting_result != None:
            cl = 'corrected'
            voting_result = voting_result.text.strip()
        else:
            voting_result = total_vote.find('p', attrs={'class': 'gruener-text'})
            if voting_result != None:
                cl = 'disputed'
                voting_result = voting_result.text.strip()
            else:
                voting_result = total_vote.find('p', attrs={'class': 'neutraler-text'})
                cl = 'neutral'
                voting_result = voting_result.text.strip()
                
    return voting_result, cl, kt_team


# find benefiting team by parsing overall voting result string
def determineBenefitingTeamOfCorretion(voting_result, cl, thread):
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
        
    return named_team, other_team, pro_contra_var


# use match result analysis to assign teams
def assignTeamsThroughMatchResults(official_res, true_res, thread):
    if int(official_res[0]) > int(true_res[0]):
        named_team = thread[1][0]
        other_team = thread[1][1]
    elif int(official_res[1]) > int(true_res[1]):
        named_team = thread[1][1]
        other_team = thread[1][0]
    elif int(official_res[0]) < int(true_res[0]):
        named_team = thread[1][1]
        other_team = thread[1][0]
    elif int(official_res[1]) < int(true_res[1]):
        named_team = thread[1][0]
        other_team = thread[1][1]
        
    return named_team, other_team


# count votes of fans of each of the teams ordered by what they voted
def determineTeamVotesOfCommunity(page, thread):
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
                    
    return num_users_team


# use voting ratios to assign teams
def assignTeamsThroughTeamVotesOfCommunity(num_users_team, thread, season_id, match_day, intervention_cnt, thread_url):
    if (num_users_team[thread[1][0]]['correct'] + num_users_team[thread[1][0]]['veto'] != 0) and \
        (num_users_team[thread[1][1]]['correct'] + num_users_team[thread[1][1]]['veto'] != 0):
        if (num_users_team[thread[1][0]]['correct'] > num_users_team[thread[1][0]]['veto'] and \
            num_users_team[thread[1][1]]['correct'] < num_users_team[thread[1][1]]['veto']) or \
            (num_users_team[thread[1][0]]['correct'] == num_users_team[thread[1][0]]['veto'] and \
            num_users_team[thread[1][1]]['correct'] < num_users_team[thread[1][1]]['veto']) or \
            (num_users_team[thread[1][0]]['correct'] > num_users_team[thread[1][0]]['veto'] and \
            num_users_team[thread[1][1]]['correct'] == num_users_team[thread[1][1]]['veto']):
            named_team = thread[1][0]
            other_team = thread[1][1]
        elif (num_users_team[thread[1][0]]['correct'] < num_users_team[thread[1][0]]['veto'] and \
            num_users_team[thread[1][1]]['correct'] > num_users_team[thread[1][1]]['veto']) or \
            (num_users_team[thread[1][0]]['correct'] == num_users_team[thread[1][0]]['veto'] and \
            num_users_team[thread[1][1]]['correct'] > num_users_team[thread[1][1]]['veto']) or \
            (num_users_team[thread[1][0]]['correct'] < num_users_team[thread[1][0]]['veto'] and \
            num_users_team[thread[1][1]]['correct'] == num_users_team[thread[1][1]]['veto']):
            named_team = thread[1][1]
            other_team = thread[1][0]
        else:
            named_team, other_team, intervention_cnt = \
                assignFromInterventionList(thread[1], season_id, match_day, intervention_cnt, thread_url)
    else:
        named_team, other_team, intervention_cnt = \
            assignFromInterventionList(thread[1], season_id, match_day, intervention_cnt, thread_url)
    
    return named_team, other_team, intervention_cnt


def getCommunityVoteResult(page, thread_url):
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
    rel_right = 100 - rel_veto
    comm_vote = [rel_right, rel_veto]
        
    return comm_vote


def getMatchResults(page):
    match = page.find('li', attrs={'class': 'aktiv'})
    
    true_res = match.find('p', attrs={'class': 'wahres_ergebnis'}).text
    true_res = true_res.split(' : ')
    
    official_res = match.find('p', attrs={'class': 'offizielles_ergebnis'})
    if official_res == None:
        official_res = true_res
    elif official_res.text == '':
        official_res = true_res
    else:
        official_res = official_res.text.split(' : ')
        
    return official_res, true_res


# find benefiting team by looking at final result vs. corrected result
# and voting result, if all corrections concern only one of the teams
def determineBenefitingTeam(page, thread_url, thread, season_id, match_day, intervention_cnt):
    comm_vote = getCommunityVoteResult(page, thread_url)
    
    official_res, true_res = getMatchResults(page)
    
    match = page.find('li', attrs={'class': 'aktiv korrektur show-for-small'})
    if match == None:
        rel_veto = 0
    else:
        corrections = match.find('h4').text
        num_corrections = int(corrections.split(' ')[0])
        
        rel_veto = comm_vote[1]
        
    if rel_veto > 50 and (abs(int(official_res[0]) - int(true_res[0])) == num_corrections or \
        abs(int(official_res[1]) - int(true_res[1])) == num_corrections):
        named_team, other_team = \
            assignTeamsThroughMatchResults(official_res, true_res, thread)
    else:
        num_users_team = determineTeamVotesOfCommunity(page, thread)
        named_team, other_team, intervention_cnt = \
            assignTeamsThroughTeamVotesOfCommunity(num_users_team, thread, season_id, match_day, intervention_cnt, thread_url)
        
    return named_team, other_team, 0, comm_vote, official_res, true_res, intervention_cnt


def getKTVotes(page, user_team_dict):
    kt_votes = page.find('div', attrs={'id': 'teilnehmerKTModal'})
    kt_votes = kt_votes.find_all('div', attrs={'class': 'teilnehmerKTModal-stimme'})
    
    kt_dict = {}
    kt_dict['richtig entschieden'] = []
    kt_dict['Veto'] = []
    kt_dict['richtig, keine Relevanz'] = []
    kt_dict['Veto, keine Relevanz'] = []
    kt_dict['keine Relevanz/unentschieden'] = []
    kt_dict['nicht zu beurteilen'] = []
    
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
        
        if user not in user_team_dict:
            user_team_dict[user] = {'team': team}
            
        kt_dict[vote].append(user)
        
    return kt_dict, user_team_dict


def getCommunityVotes(page, user_team_dict):
    page = page.find('div', attrs={'id': 'teilnehmerModal'})
    
    comm_votes = page.find_all('div', attrs={'class': 'three columns ac'})
    if comm_votes == []:
        comm_votes = page.find_all('div', attrs={'class': 'four columns ac'})
    else:
        comm_votes = comm_votes[:2]
    
    comm_dict = {}
    comm_dict['richtig entschieden'] = []
    comm_dict['Veto'] = []
    comm_dict['keine Relevanz, unentschieden'] = []
    
    for vote_class in comm_votes:
        vote = vote_class.find('th').text.strip()
        if 'keine Relevanz' in vote:
            vote = 'keine Relevanz, unentschieden'

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
        
            if user not in user_team_dict:
                user_team_dict[user] = {'team': team}
                
            comm_dict[vote].append(user)
                    
    return comm_dict, user_team_dict


# extract information from threads
def getThreadDetails(threads, user_team_dict, season_id, match_day, intervention_cnt, new_intervention_list):
    print('-- get voting results from', str(len(threads)), 'threads')
    matchday_threads = []
    for thread in threads:             
        thread_url = base_url + thread[0] + '&page=1'
        response = sendRequest(thread_url)
        page = BeautifulSoup(response.data, features="html5lib")
        
        thread_data = {}
        thread_data['url'] = thread_url
        thread_data['teams'] = thread[1]
        thread_data['errors'] = 0 
        
        error_check = page.find('div', attrs={'class': 'nine columns'})
        try:
          error_check = error_check.find('h1').text
          print('## err:', error_check, 'in called thread')
          if error_check == 'Error 500':
            thread_data['errors'] = 500 # never gets written
            thread_data['class'] = None
            thread_data['vote_details'] = {}
            thread_data['match_results'] = {}
            matchday_threads.append(thread_data)
            continue
        except:
            pass
        
        voting_result, cl, kt_team = getVotingResult(page, thread)

        thread_data['class'] = cl
                
        if cl == 'corrected':
            named_team, other_team, pro_contra_var = \
                determineBenefitingTeamOfCorretion(voting_result, cl, thread)
            comm_vote = getCommunityVoteResult(page, thread_url)
            official_res, true_res = getMatchResults(page)
        elif cl == 'disputed' or cl == 'neutral' or cl == 'no_kt_vote':
            curr_intervention_cnt = intervention_cnt
            named_team, other_team, pro_contra_var, comm_vote, official_res, true_res, intervention_cnt = \
                determineBenefitingTeam(page, thread_url, thread, season_id, match_day, intervention_cnt)
            if curr_intervention_cnt == intervention_cnt-1:
                new_intervention_list.append( (named_team, match_day) )
                
        if kt_team == True:
            print('-- [', thread[1][0], '-', thread[1][1], '] parsing KT team votes')
            kt_dict, user_team_dict = getKTVotes(page, user_team_dict)
        
        print('-- [', thread[1][0], '-', thread[1][1], '] parsing community user votes')
        comm_dict, user_team_dict = getCommunityVotes(page, user_team_dict)
        
        vote_details = {}
        vote_details['voting_result'] = voting_result
        vote_details['community_vote'] = comm_vote
        vote_details['pro_contra_var'] = pro_contra_var
        vote_details['named_team'] = named_team
        vote_details['other_team'] = other_team
        if kt_team == True:
            vote_details['kt_votes'] = kt_dict
        else:
            vote_details['kt_votes'] = {}
        vote_details['comm_votes'] = comm_dict
        
        thread_data['vote_details'] = vote_details
        thread_data['match_results'] = {}
        thread_data['match_results']['official'] = official_res
        thread_data['match_results']['true'] = true_res
    
        matchday_threads.append(thread_data)
    
    return matchday_threads, user_team_dict, intervention_cnt, new_intervention_list


# iterate through match days
def iterateThroughMatchdays(season_url, season_id, league):
    user_team_dict = {}
    matchdays = {}
    intervention_cnt = 0
    new_intervention_list = []
    
    for match_day in range(1,MATCHDAYS+1):
        print('Match day:', match_day)
        matchday_url = season_url + '&spieltag=' + str(match_day)
        
        matches = getRelevantMatches(matchday_url)
        threads = getDisputedThreads(matches)
        matchday_threads, user_team_dict, intervention_cnt, new_intervention_list = \
            getThreadDetails(threads, user_team_dict, season_id, match_day, intervention_cnt, new_intervention_list)
        
        matchdays[match_day] = matchday_threads

    print(new_intervention_list)
    
    return matchdays, user_team_dict


# iterate through seasons
for id_pos in range(len(season_ids['BL1'])+len(season_ids['BL2'])):
    if id_pos < len(season_ids['BL1']):
        season_id = season_ids['BL1'][id_pos][0]
        season_year = season_ids['BL1'][id_pos][1]
        league = 1
    else:
        season_id = season_ids['BL2'][id_pos-len(season_ids['BL1'])][0]
        season_year = season_ids['BL2'][id_pos-len(season_ids['BL1'])][1]
        league = 2
        
    season_url = base_url + '/index/index/liga/' + str(league) + '?saisonId=' + str(season_id)
    
    print('Season id', season_id)
    matchday_data, users = iterateThroughMatchdays(season_url, season_id, league)
    season_data = {'id': season_id, 'season_year': season_year, 'league': league}
    
    with open('data_season_BL' + str(league) + '_s' + season_year + '.pickle', 'wb') as f:
        pickle.dump([season_data, users, matchday_data], f)
