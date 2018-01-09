# -*- coding:utf-8 -*-
import pandas as pd
import math
import csv
import random
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression

base_elo = 1600
team_elos = {}
team_stats = {}
X = []
y = []
folder = 'data'

# \u8ba1\u7b97\u6bcf\u4e2a\u7403\u961f\u7684elo\u503c
def calc_elo(win_team, lose_team):
    winner_rank = get_elo(win_team)
    loser_rank = get_elo(lose_team)

    rank_diff = winner_rank - loser_rank
    exp = (rank_diff  * -1) / 400
    odds = 1 / (1 + math.pow(10, exp))
    # \u6839\u636erank\u7ea7\u522b\u4fee\u6539K\u503c
    if winner_rank < 2100:
        k = 32
    elif winner_rank >= 2100 and winner_rank < 2400:
        k = 24
    else:
        k = 16
    new_winner_rank = round(winner_rank + (k * (1 - odds)))
    new_rank_diff = new_winner_rank - winner_rank
    new_loser_rank = loser_rank - new_rank_diff

    return new_winner_rank, new_loser_rank

# \u6839\u636e\u6bcf\u652f\u961f\u4f0d\u7684Miscellaneous Opponent\uff0cTeam\u7edf\u8ba1\u6570\u636ecsv\u6587\u4ef6\u8fdb\u884c\u521d\u59cb\u5316
def initialize_data(Mstat, Ostat, Tstat):
    new_Mstat = Mstat.drop(['Rk', 'Arena'], axis=1)
    new_Ostat = Ostat.drop(['Rk', 'G', 'MP'], axis=1)
    new_Tstat = Tstat.drop(['Rk', 'G', 'MP'], axis=1)

    team_stats1 = pd.merge(new_Mstat, new_Ostat, how='left', on='Team')
    team_stats1 = pd.merge(team_stats1, new_Tstat, how='left', on='Team')

    print team_stats1.info()
    return team_stats1.set_index('Team', inplace=False, drop=True)

def get_elo(team):
    try:
        return team_elos[team]
    except:
        # \u5f53\u6700\u521d\u6ca1\u6709elo\u65f6\uff0c\u7ed9\u6bcf\u4e2a\u961f\u4f0d\u6700\u521d\u8d4bbase_elo
        team_elos[team] = base_elo
        return team_elos[team]

def  build_dataSet(all_data):
    print("Building data set..")
    for index, row in all_data.iterrows():

        Wteam = row['WTeam']
        Lteam = row['LTeam']

        #\u83b7\u53d6\u6700\u521d\u7684elo\u6216\u662f\u6bcf\u4e2a\u961f\u4f0d\u6700\u521d\u7684elo\u503c
        team1_elo = get_elo(Wteam)
        team2_elo = get_elo(Lteam)

        # \u7ed9\u4e3b\u573a\u6bd4\u8d5b\u7684\u961f\u4f0d\u52a0\u4e0a100\u7684elo\u503c
        if row['WLoc'] == 'H':
            team1_elo += 100
        else:
            team2_elo += 100

        # \u628aelo\u5f53\u4e3a\u8bc4\u4ef7\u6bcf\u4e2a\u961f\u4f0d\u7684\u7b2c\u4e00\u4e2a\u7279\u5f81\u503c
        team1_features = [team1_elo]
        team2_features = [team2_elo]

        # \u6dfb\u52a0\u6211\u4eec\u4ecebasketball reference.com\u83b7\u5f97\u7684\u6bcf\u4e2a\u961f\u4f0d\u7684\u7edf\u8ba1\u4fe1\u606f
        for key, value in team_stats.loc[Wteam].iteritems():
            team1_features.append(value)
        for key, value in team_stats.loc[Lteam].iteritems():
            team2_features.append(value)

        # \u5c06\u4e24\u652f\u961f\u4f0d\u7684\u7279\u5f81\u503c\u968f\u673a\u7684\u5206\u914d\u5728\u6bcf\u573a\u6bd4\u8d5b\u6570\u636e\u7684\u5de6\u53f3\u4e24\u4fa7
        # \u5e76\u5c06\u5bf9\u5e94\u76840/1\u8d4b\u7ed9y\u503c
        if random.random() > 0.5:
            X.append(team1_features + team2_features)
            y.append(0)
        else:
            X.append(team2_features + team1_features)
            y.append(1)

        # \u6839\u636e\u8fd9\u573a\u6bd4\u8d5b\u7684\u6570\u636e\u66f4\u65b0\u961f\u4f0d\u7684elo\u503c
        new_winner_rank, new_loser_rank = calc_elo(Wteam, Lteam)
        team_elos[Wteam] = new_winner_rank
        team_elos[Lteam] = new_loser_rank

    return np.nan_to_num(X), np.array(y)

def predict_winner(team_1, team_2, model):
    features = []

    # team 1\uff0c\u5ba2\u573a\u961f\u4f0d
    features.append(get_elo(team_1))
    for key, value in team_stats.loc[team_1].iteritems():
        features.append(value)

    # team 2\uff0c\u4e3b\u573a\u961f\u4f0d
    features.append(get_elo(team_2) + 100)
    for key, value in team_stats.loc[team_2].iteritems():
        features.append(value)

    features = np.nan_to_num(features)
    return model.predict_proba([features])

if __name__ == '__main__':

    Mstat = pd.read_csv(folder + '/15-16Miscellaneous_Stat.csv')
    Ostat = pd.read_csv(folder + '/15-16Opponent_Per_Game_Stat.csv')
    Tstat = pd.read_csv(folder + '/15-16Team_Per_Game_Stat.csv')

    team_stats = initialize_data(Mstat, Ostat, Tstat)

    result_data = pd.read_csv(folder + '/2015-2016_result.csv')
    X, y = build_dataSet(result_data)

    # \u8bad\u7ec3\u7f51\u7edc\u6a21\u578b
    print("Fitting on %d game samples.." % len(X))

    model = LogisticRegression()
    model.fit(X, y)

    #\u5229\u752810\u6298\u4ea4\u53c9\u9a8c\u8bc1\u8ba1\u7b97\u8bad\u7ec3\u6b63\u786e\u7387
    print("Doing cross-validation..")
    print(cross_val_score(model, X, y, cv = 10, scoring='accuracy', n_jobs=-1).mean())


    #\u5229\u7528\u8bad\u7ec3\u597d\u7684model\u572816-17\u5e74\u7684\u6bd4\u8d5b\u4e2d\u8fdb\u884c\u9884\u6d4b
    print('Predicting on new schedule..')
    schedule1617 = pd.read_csv(folder + '/16-17Schedule.csv')
    result = []
    for index, row in schedule1617.iterrows():
        team1 = row['Vteam']
        team2 = row['Hteam']
        pred = predict_winner(team1, team2, model)
        prob = pred[0][0]
        if prob > 0.5:
            winner = team1
            loser = team2
            result.append([winner, loser, prob])
        else:
            winner = team2
            loser = team1
            result.append([winner, loser, 1 - prob])

    with open('16-17Result.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['win', 'lose', 'probability'])
        writer.writerows(result)









