import csv

import numpy as np
from sklearn.linear_model import LinearRegression


# This class was just good to chang the imported data in "HisotryImported"
def allInOneFile():
    data = open("allData/data/Chess/chessData.csv")
    data = data.read()
    data = data.split("\n")
    data.remove(data[0])
    data.remove(data[-1])
    data_y = []
    for p in range(len(data)):
        col_all = []
        col = data[p].split(",")
        col_two = col[0].split(" ")
        col_all.append(col_two[0] + " " + col_two[1] + " " + col_two[2])
        col_all.append(col[1])
        col_all.append("-")
        col_all.append(0)
        col_all.append(0)
        data_y.append(col_all)
    for i in range(0, len(data_y)):
        data_y[i][1] = data_y[i][1].replace('#', '')
    data_y.insert(0, ["FEN", "ImportedEvaluation", "Evaluation", "Wins", "Plays"])
    with open('HistoryImported.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data_y)
    print ("Done!")
    return data_y


def seperateFiles():
    data = open("allData/data/Chess/chessData.csv")
    data = data.read()
    data = data.split("\n")
    data.remove(data[0])
    data.remove(data[-1])
    data_b_r = []
    data_b = []
    data_w_r = []
    data_w = []
    for p in range(len(data)):
        col_all = []
        col = data[p].split(",")
        col_two = col[0].split(" ")
        col_all.append(col_two[0] + " " + col_two[1] + " " + col_two[2])
        col_all.append(col[1])
        col_all.append("-")
        col_all.append(0)
        col_all.append(0)
        if col_two[1] == "b":
            if col_two[2] == "-":
                data_b.append(col_all)
            else:
                data_b_r.append(col_all)
        elif col_two[1] == "w":
            if col_two[2] == "-":
                data_w.append(col_all)
            else:
                data_w_r.append(col_all)

    for i in range(0, len(data_b)):
        data_b[i][1] = data_b[i][1].replace('#', '')
    for i in range(0, len(data_b_r)):
        data_b_r[i][1] = data_b_r[i][1].replace('#', '')
    for i in range(0, len(data_w)):
        data_w[i][1] = data_w[i][1].replace('#', '')
    for i in range(0, len(data_w_r)):
        data_w_r[i][1] = data_w_r[i][1].replace('#', '')
    data_b.insert(0, ["FEN", "ImportedEvaluation", "Evaluation", "Wins", "Plays"])
    data_b_r.insert(0, ["FEN", "ImportedEvaluation", "Evaluation", "Wins", "Plays"])
    data_w.insert(0, ["FEN", "ImportedEvaluation", "Evaluation", "Wins", "Plays"])
    data_w_r.insert(0, ["FEN", "ImportedEvaluation", "Evaluation", "Wins", "Plays"])
    with open('HistoryImported_b.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data_b)
    with open('HistoryImported_b_r.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data_b_r)
    with open('HistoryImported_w.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data_w)
    with open('HistoryImported_w_r.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data_w_r)
    print ("Done!")

    print(len(data_b))
    print(len(data_b_r))
    print(len(data_w))
    print(len(data_w_r))



