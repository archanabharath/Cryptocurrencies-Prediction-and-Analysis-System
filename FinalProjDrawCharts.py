'''
Project : CryptoCurrencies Prediction and Analysis System
Author : Archana Subramaniyan
Course : ITMD 513 Open Source Programming
File : FinalProjBTCPred.py
About : This is the module that generates different charts on different data of a variety of cryptocoins

'''

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import csv


#Barchart of average volume of coins
def bar_chart(coins_list, c_type):
    df = pd.read_csv("all-cryptocoins.csv", delimiter=',')
    df_vol_mcap = df.drop(['Date','Open','High','Close','Low'],axis=1)
    q2 = "Symbol in ["
    for i in range(0,coins_list.__len__()):
        if i == coins_list.__len__()-1:
            q2 += '"'+coins_list[i].split('-')[0]+'"'+"]"
        else:
            q2 += '"'+coins_list[i].split('-')[0]+'"'+ ","



    df_vol_short = df_vol_mcap.query(q2)

    a = df_vol_short.groupby('Symbol')['Volume'].mean()
    b = df_vol_short.groupby('Symbol')['Market Cap'].mean()
    if c_type == 'Volume':
        ax = a.plot.bar()
        ax.set(xlabel='Coin', ylabel='Average Volume')
        ax.legend()
        ax.set(title="Crypto Coins Average Volume Chart")


    elif c_type == 'Market':
        bx = b.plot.bar()
        bx.set(xlabel='Coin', ylabel='Average Market Cap')
        bx.legend()
        bx.set(title="Crypto Coins Average Market Cap Chart")

    barplot_name = 'Barplot.png'
    plt.savefig(barplot_name)
    plt.close()
    return barplot_name


#generate box plot of HIGH price of one or different coins
def box_plot(box_coins_list):

    df = pd.read_csv("all-coins-HIGH-price.csv", delimiter=',')

    df_filter = []

    for i in range(0,box_coins_list.__len__()):
        df_filter.append("High-"+box_coins_list[i].split('-')[0])

    df_high_sel = df[df_filter]
    print('----------------------------------HIGH Price Statistics-------------------------')
    print(df_high_sel.describe())

    ax = sns.boxplot(data=df_high_sel)
    ax.set_ylabel("Coin's high price of the day")
    ax.set_title("Cryptocurrencies HIGH price distribution")
    ax.grid()
    boxplot_name = 'Boxplot.png'
    plt.savefig(boxplot_name)
    plt.close()
    return boxplot_name

#generate scatter plot of the yearly average close price of different coins
def scatter_plot(coin):
    file = coin+"-scatter-close.csv"
    with open(file, "r") as f:
        reader = csv.reader(f)
        close_list = list(reader)


    count_18 = 0
    sum_18 = 0
    count_17 = 0
    sum_17 = 0
    count_16 = 0
    sum_16 = 0
    count_15 = 0
    sum_15 = 0
    count_14 = 0
    sum_14 = 0
    count_13 = 0
    sum_13 = 0

    for i in range(1, close_list.__len__()):
        if close_list[i][0].split('-')[1] == '18':
            count_18 += 1
            sum_18 += float(close_list[i][1])
        elif close_list[i][0].split('-')[1] == '17':
            count_17 += 1
            sum_17 += float(close_list[i][1])
        elif close_list[i][0].split('-')[1] == '16':
            count_16 += 1
            sum_16 += float(close_list[i][1])
        elif close_list[i][0].split('-')[1] == '15':
            count_15 += 1
            sum_15 += float(close_list[i][1])
        elif close_list[i][0].split('-')[1] == '14':
            count_14 += 1
            sum_14 += float(close_list[i][1])
        elif close_list[i][0].split('-')[1] == '13':
            count_13 += 1
            sum_13 += float(close_list[i][1])

    avg_list = {}
    if count_18 > 0:
        avg_18 = sum_18 / count_18
        avg_list[2018] = avg_18
    if count_17 > 0:
        avg_17 = sum_17/count_17
        avg_list[2017] = avg_17
    if count_16 > 0:
        avg_16 = sum_16/count_16
        avg_list[2016] = avg_16
    if count_15 > 0:
        avg_15 = sum_15/count_15
        avg_list[2015] = avg_15
    if count_14 > 0:
        avg_14 = sum_14/count_14
        avg_list[2014] = avg_14
    if count_13 > 0:
        avg_13 = sum_13/count_13
        avg_list[2013] = avg_13



    n = avg_list.__len__()

    colors = np.random.rand(n)
    area = (30 * np.random.rand(n)) ** 2
    plt.scatter(avg_list.keys(), avg_list.values(), s=area, c=colors, alpha=1)
    plt.locator_params(axis='x', nbins=avg_list.__len__())
    plt.xlabel('Year')
    plt.ylabel('Yearly average of close price')
    plt.title('Scatter plot of '+coin.capitalize()+' yearly average close price')
    image_nm = coin.capitalize()+"-scatter.png"
    plt.savefig(image_nm)
    plt.close()
    return image_nm
