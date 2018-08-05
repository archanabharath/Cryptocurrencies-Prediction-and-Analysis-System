'''
Project : CryptoCurrencies Prediction and Analysis System
Author : Archana Subramaniyan
Course : ITMD 513 Open Source Programming
File : FinalProjETHPred.py
About : This is the module that builds LSTM prediction model for predicting future prices of Ethereum data

'''

import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import math
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# this function creates two datasets which would contain the close price values at times t and t+1 respectively
def create_test_train(df_close_scaled):
    data_t = []
    data_t_next = []
    for i in range(len(df_close_scaled) - 1):
        data_t.append(df_close_scaled[i])
        data_t_next.append(df_close_scaled[i + 1])

    return np.asarray(data_t), np.array(data_t_next)


#function that builds a LSTM model covering from data preparation to fit the model to predicting and plotting
#full data is split on 70% as train data and 25% as test data
def eth_daily_pred_lstm(df_close_float, days_count):

    np.random.seed(10)

    lstm_scaler = MinMaxScaler(feature_range=(0, 1))

    df_close_scaled = lstm_scaler.fit_transform(df_close_float)


    # this function creates two datasets which would contain the btc close value at time t and t+1 respectively


    X, y = create_test_train(df_close_scaled)

    # creating test and train datasets by splitting the original data in 80/20 ratio. This is done using a built-in
    # function available in the scikit-learn package

    train_t, test_t, train_nextT, test_nextT = train_test_split(X, y, test_size=0.30, shuffle=False)

    # LSTM takes input in the form of samples,time steps and features
    # so the test and train datasets are to be reshaped to the above structure

    train_t = np.reshape(train_t, (train_t.shape[0], 1, train_t.shape[1]))
    test_t = np.reshape(test_t, (test_t.shape[0], 1, test_t.shape[1]))

    # creating a LSTM network


    model = Sequential()
    model.add(LSTM(20, input_shape=(1, 1)))  # 20 is best fit

    model.add(Dense(1, activation = 'linear'))

    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    model.fit(train_t, train_nextT, epochs=300, batch_size=40, verbose=1)  # 300,33 is best fit so far
    model.save('./savedmodel')

    # making predictions


    trainPredict= model.predict(train_t)

    testPredict = model.predict(test_t)
    futurePredict = model.predict(np.asarray([[testPredict[-1]]]))
    fut_pred_trans = lstm_scaler.inverse_transform(futurePredict)
    testPredict_list = testPredict.tolist()
    testPredict_list.append([futurePredict])
    test_t_list = test_t.tolist()
    test_t_list.append([futurePredict])
    test_t_new = np.append(test_t, [futurePredict])
    test_t_new = np.reshape(test_t_new, (test_t_new.shape[0], 1, test_t.shape[1]))

    a = futurePredict


    if days_count == 1:
        futurePredict_new = model.predict(np.asarray([a]))
        fut_pred_trans = lstm_scaler.inverse_transform(futurePredict_new)
        test_t_new = np.append(test_t_new, [futurePredict_new])
        test_t_new = np.reshape(test_t_new, (test_t_new.shape[0], 1, test_t.shape[1]))
        a = futurePredict_new
        prediction_that_date = fut_pred_trans
        prediction_tomo = fut_pred_trans
    elif days_count > 1:
        for i in range(0, days_count):

            futurePredict_new = model.predict(np.asarray([a]))
            fut_pred_trans = lstm_scaler.inverse_transform(futurePredict_new)
            test_t_new = np.append(test_t_new, [futurePredict_new])
            test_t_new = np.reshape(test_t_new, (test_t_new.shape[0], 1, test_t.shape[1]))
            a = futurePredict_new

            if i == 0:
                prediction_tomo = fut_pred_trans

            if i == days_count - 1:
                prediction_that_date = fut_pred_trans

    # apply inverse transformation on the predicted data which is still in 0 to 1 scale
    trainPredict = lstm_scaler.inverse_transform(trainPredict)
    train_nextT = lstm_scaler.inverse_transform(train_nextT)
    testPredict = lstm_scaler.inverse_transform(testPredict)
    test_nextT = lstm_scaler.inverse_transform(test_nextT)
    futurePredict = lstm_scaler.inverse_transform(futurePredict)

    print("price of tomorrow: ", round(prediction_tomo[0][0],2))


    # calculating RMSE to evaluate the performance of the model
    print("-----------------------Ethereum Prediction model Accuracy ---------------------")
    train_score = math.sqrt(mean_squared_error(train_nextT[:, 0], trainPredict[:, 0]))
    print("Train predictions RMSE: %.2f" % (train_score))
    test_score = math.sqrt(mean_squared_error(test_nextT[:, 0], testPredict[:, 0]))
    print("Test predictions RMSE: %.2f" % (test_score))


    # predictions plot
    trainPredictPlot = np.empty_like(df_close_scaled)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[1:len(trainPredict) + 1, :] = trainPredict

    # shift test predictions for plotting
    testPredictPlot = np.empty_like(df_close_scaled)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(trainPredict):len(df_close_scaled) - 1, :] = testPredict

    # plot baseline and predictions
    plt.plot(lstm_scaler.inverse_transform(df_close_scaled), label = 'Actual')
    plt.xlabel("Time")
    plt.ylabel("ETH Close Price")
    plt.title("Ethereum Close Price Trend Graph")
    plt.plot(trainPredictPlot, label = 'Train Predictions')
    plt.plot(testPredictPlot, label = 'Test Predictions')
    plt.legend()
    eth_trend_img = "ETH-trend-plot.png"
    plt.savefig(eth_trend_img)
    plt.close()

    return round(futurePredict[0][0], 2), round(prediction_tomo[0][0], 2),round(prediction_that_date[0][0],2), eth_trend_img