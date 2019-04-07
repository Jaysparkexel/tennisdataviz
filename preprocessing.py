#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import numpy as np


# In[2]:


data = pd.read_csv("10yearAUSOpenMatches.csv")


# In[3]:


data = data.drop(columns=['gender', 'firstServe1', 'firstServe2', 'ace1', 'ace2','double1', 'double2', 'firstPointWon1', 'firstPointWon2', 'secPointWon1', 'secPointWon2', 'fastServe1', 'fastServe2',
       'avgFirstServe1', 'avgFirstServe2', 'avgSecServe1', 'avgSecServe2',
       'break1', 'break2', 'return1', 'return2', 'total1', 'total2', 'winner1',
       'winner2', 'error1', 'error2', 'net1', 'net2'])


# In[4]:


def get_name_node(play, score, round_nm=0):
    x = {
        "name":play,
        "round":round_nm,
        "children":[],
        "match": {
            "w1": score["w1"],
            "w2": score["w2"],
            "w3": score["w3"],
            "w4": score["w4"],
            "w5": score["w5"],
            "l1": score["l1"],
            "l2": score["l2"],
            "l3": score["l3"],
            "l4": score["l4"],
            "l5": score["l5"]  
        }
    }
    return x

def getScore(result_str):
    score = {
    "w1":0,
    "w2":0,
    "w3":0,
    "w4":0,
    "w5":0,
    "l1":0,
    "l2":0,
    "l3":0,
    "l4":0,
    "l5":0
    }
    if len(result_str) == 0:
        return score
    strp_str = result_str.split(" ")
    if 'ret' in strp_str[-1]:
        del strp_str[-1]
    
    for i in range(len(strp_str)):
        sc = strp_str[i].split("-")
        j = i + 1
        score["w"+str(j)] = sc[0]
        score["l"+str(j)] = sc[1]
        
    return score


# In[5]:


years = [2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014]

for y in years:
    
    year_data = data.loc[data['year'] == y]
    year_data = year_data.sort_values(by=['winner'])


    final_winner = year_data.loc[year_data['round'] =='Final',['winner','player1', 'player2','results']]
    semi_winner = year_data.loc[year_data['round'] =='semi',['winner','player1', 'player2','results']]
    quarter_winner = year_data.loc[year_data['round'] =='quarter',['winner','player1', 'player2','results']]
    fourth_winner = year_data.loc[year_data['round'] =='Fourth',['winner','player1', 'player2','results']]
    third_winner = year_data.loc[year_data['round'] =='Third',['winner','player1', 'player2','results']]
    second_winner = year_data.loc[year_data['round'] =='Second',['winner','player1', 'player2','results']]
    first_winner = year_data.loc[year_data['round'] =='First',['winner','player1', 'player2','results']]


    for index, row in final_winner.iterrows():
        winner = row['winner']
        first = row['player1']
        second = row['player2']
        winner_score_str = row['results']
        winner_score = getScore(winner_score_str)
        first_score_str = semi_winner.loc[semi_winner['winner']==first,['results']].values[0][0]
        first_score = getScore(first_score_str)
        second_score_str = semi_winner.loc[semi_winner['winner']==second,['results']].values[0][0]
        second_score =getScore(second_score_str)
        first_node = get_name_node(first, first_score,7)
        second_node = get_name_node(second, second_score, 7)
        global_json = get_name_node(winner, winner_score,8)
        global_json['children'] = [first_node, second_node]

    i = 0
    semi_dict={}
    for index, row in semi_winner.iterrows():
        winner = row['winner']
        first = row['player1']
        second = row['player2']
        first_score_str = quarter_winner.loc[quarter_winner['winner']==first,['results']].values[0][0]
        first_score = getScore(first_score_str)
        second_score_str = quarter_winner.loc[quarter_winner['winner']==second,['results']].values[0][0]
        second_score =getScore(second_score_str)
        first_node = get_name_node(first, first_score, 6)
        second_node = get_name_node(second, second_score, 6)
        global_json['children'][i]['children'] = [first_node, second_node]
        semi_dict[first] = [i, 0]
        semi_dict[second] = [i, 1]
        i = i+1

    quarter_dict={}
    for index, row in quarter_winner.iterrows():
        winner = row['winner']
        first = row['player1']
        second = row['player2']
        first_score_str = fourth_winner.loc[fourth_winner['winner']==first,['results']].values[0][0]
        first_score = getScore(first_score_str)
        second_score_str = fourth_winner.loc[fourth_winner['winner']==second,['results']].values[0][0]
        second_score =getScore(second_score_str)
        first_node = get_name_node(first, first_score, 5)
        second_node = get_name_node(second, second_score, 5)
        rank = semi_dict[winner]
        rank1 = rank.copy()
        rank1.append(0)
        rank2 = rank.copy()
        rank2.append(1)
        quarter_dict[first] = rank1
        quarter_dict[second] = rank2
        global_json['children'][rank[0]]['children'][rank[1]]['children'] = [first_node, second_node]

    fourth_dict={}
    for index, row in fourth_winner.iterrows():
        winner = row['winner']
        first = row['player1']
        second = row['player2']
#         print(winner)
#         print(first)
#         print(second)
#         print("-------")
#         try:
        first_score_str = third_winner.loc[third_winner['winner']==first,['results']].values[0][0]
        first_score = getScore(first_score_str)
#         except:
#             first_score = getScore("")
#         try:
        second_score_str = third_winner.loc[third_winner['winner']==second,['results']].values[0][0]
        second_score =getScore(second_score_str)
#         except:
#             second_score = getScore("")
        first_node = get_name_node(first, first_score, 4)
        second_node = get_name_node(second, second_score, 4)
        rank = quarter_dict[winner]
        rank1 = rank.copy()
        rank1.append(0)
        rank2 = rank.copy()
        rank2.append(1)
        fourth_dict[first] = rank1
        fourth_dict[second] = rank2
        global_json['children'][rank[0]]['children'][rank[1]]['children'][rank[2]]['children'] = [first_node, second_node]

    third_dict={}
    for index, row in third_winner.iterrows():
        winner = row['winner']
        first = row['player1']
        second = row['player2']
#         print(winner)
#         print(first)
#         print(second)
#         print("-------")
        
#         try:
        first_score_str = second_winner.loc[second_winner['winner']==first,['results']].values[0][0]
        first_score = getScore(first_score_str)
#         except:
#             first_score = getScore("")
        second_score_str = second_winner.loc[second_winner['winner']==second,['results']].values[0][0]
        second_score =getScore(second_score_str)
        first_node = get_name_node(first, first_score, 3)
        second_node = get_name_node(second, second_score, 3)
        rank = fourth_dict[winner]
        rank1 = rank.copy()
        rank1.append(0)
        rank2 = rank.copy()
        rank2.append(1)
        third_dict[first] = rank1
        third_dict[second] = rank2
        global_json['children'][rank[0]]['children'][rank[1]]['children'][rank[2]]['children'][rank[3]]['children'] = [first_node, second_node]
            
    second_dict={}
    for index, row in second_winner.iterrows():
        winner = row['winner']
        first = row['player1']
        second = row['player2']
#         print(winner)
#         print(first)
#         print(second)
#         print("-------")
#         try:
        first_score_str = first_winner.loc[first_winner['winner']==first,['results']].values[0][0]
        first_score = getScore(first_score_str)
#         except:
#             first_score = getScore("")
#         try:
        second_score_str = first_winner.loc[first_winner['winner']==second,['results']].values[0][0]
        second_score =getScore(second_score_str)
#         except:
#             second_score = getScore("")
        first_node = get_name_node(first, first_score, 2)
        second_node = get_name_node(second, second_score, 2)
        flag = 0
        rank = third_dict[winner]
        rank1 = rank.copy()
        rank1.append(0)
        rank2 = rank.copy()
        rank2.append(1)
        second_dict[first] = rank1
        second_dict[second] = rank2
        global_json['children'][rank[0]]['children'][rank[1]]['children'][rank[2]]['children'][rank[3]]['children'][rank[4]]['children'] = [first_node, second_node]


    first_dict={}
    for index, row in first_winner.iterrows():
        winner = row['winner']
        first = row['player1']
        second = row['player2']
        first_score = getScore("")
        second_score =getScore("")
        first_node = get_name_node(first, first_score, 1)
        second_node = get_name_node(second, second_score, 1)
#         flag = 0
#         try:
        rank = second_dict[winner]
#         except: 
#             flag = 1
#         if flag == 0:
        rank1 = rank.copy()
        rank1.append(0)
        rank2 = rank.copy()
        rank2.append(1)
        global_json['children'][rank[0]]['children'][rank[1]]['children'][rank[2]]['children'][rank[3]]['children'][rank[4]]['children'][rank[5]]['children'] = [first_node, second_node]
    
    fname = str(y) +".json"
    with open(fname, 'w') as outfile:
        json.dump(global_json, outfile)


# In[ ]:




