'''
Project : CryptoCurrencies Prediction and Analysis System
Author : Archana Subramaniyan
Course : ITMD 513 Open Source Programming
File : FinalProjFrames.py
About : This is the driver module that handles all frame navigations and invokes other modules
          for respective functionalities
Functionalities designed:
    1) Login - user enters username and PIN to login the application.
               two step validation - PIN and Access code - done before accessing the application
    2) Registration - users can register in the registration frame to register and get access to the application
    3) Menu - After 2 step validation, a menu frame is thrown which contains the different operations
              a user can execute in this application. Two categories of menu - Prediction and Visualization
    4) Prediction - options available here are used to predict the future CLOSE price of the cryptocurrencies:
                    Bitcoin, Ethereum, LiteCoin.
    5) Visualization - options in this category are used to visualize the distribution of different prices of
                       different cryptocurrencies. visualizations are rendered in the form of bar charts, scatter plots
                       and box plots

'''
import tkinter as tk
from tkinter import messagebox
import os
import FinalProjDBAccess as fd
import FinalProjBTCPred as btc_pred
import FinalProjETHPred as eth_pred
import FinalProjLTCPred as ltc_pred
import FinalProjDrawCharts as charts
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import datetime as dt
import hashlib, uuid
from PIL import Image, ImageTk
import webbrowser
import warnings
warnings.filterwarnings("ignore")

today_date_default = time.strftime("%x")
date_mm = today_date_default.split("/")[0]
date_dd  = today_date_default.split("/")[1]
today_date_fmt_default = date_mm+"/"+date_dd+"/2018"

LARGE_FONT= ("Verdana", 16)
MEDIUM_FONT = ("Verdana", 14)
SMALL_FONT = ("Verdana", 12)

hist_btc = "Bitcoinhistplot.png"
trend_btc = "Bitcoinplot.png"
hist_eth = "Ethereumhistplot.png"
trend_eth = "Ethereumplot.png"


global scatter_fig, trend_fig, hist_fig, img, tkimage, hist_img, pred_img,tkimagehist, tkimagepred
global trend_fig_1,pred_img_1, tkimagepred_1


#controller class for all frames
class PageController(tk.Tk):


    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (LoginFrame, MenuFrame, RegisterFrame, DailyPredFrame, BarChartFrame, BoxPlotFrame, ScatterPlotFrame):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)


    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


#Login frame to help a user to login to the application
class LoginFrame(tk.Frame):


    def __init__(self, parent, controller):


        global usernameloginVar, PINloginVar, accessVar, labela,access_code, button3

        tk.Frame.__init__(self, parent)

        app_title = tk.Label(self, text="CryptoCurrency Predictions and Analysis System", font=LARGE_FONT)
        app_title.place(x=600,y=10, border='outside')


        img_l = Image.open('cryptos-login.png')
        im_l_width = img_l.size[0]
        im_l_height = img_l.size[1]
        self.tkimage_l = ImageTk.PhotoImage(img_l)
        label_login_image = tk.Label(self, image=self.tkimage_l, font=SMALL_FONT)
        label_login_image.place(x=100,y=200, width=im_l_width, height=im_l_height)

        label1 = tk.Label(self, text="UserName:", font= LARGE_FONT)
        label1.place(x=1200,y=200)
        usernameloginVar = tk.StringVar()
        username = tk.Entry(self, textvariable=usernameloginVar, font= LARGE_FONT)
        username.place(x=1350,y=200)

        label2 = tk.Label(self, text="PIN:", font= LARGE_FONT)
        label2.place(x=1200,y=350)
        PINloginVar = tk.StringVar()
        userpin = tk.Entry(self, textvariable=PINloginVar, font= LARGE_FONT, show = '*')
        userpin.place(x=1350,y=350)

        labela = tk.Label(self, text="Access code:", font=LARGE_FONT)
        labela.place(x=700,y=500)
        labela.place_forget()
        accessVar = tk.StringVar()
        access_code = tk.Entry(self, textvariable=accessVar, font=LARGE_FONT, show='*')
        access_code.place(x=900,y=500)
        access_code.place_forget()

        btn1 = tk.Button(self, text="Login", command=login_user, font= MEDIUM_FONT)
        btn1.place(x=1200,y=700)

        button2 = tk.Button(self, text="Register", command=lambda: controller.show_frame(RegisterFrame), font= MEDIUM_FONT)
        button2.place(x=1400,y=700)

        button3 = tk.Button(self, text="Verify Access", command=verify_access, font=MEDIUM_FONT)
        button3.place(x=1600, y=700)
        button3.place_forget()

        quitbtn = tk.Button(self, text=" Quit ", command=close_app, font= LARGE_FONT)
        quitbtn.place(x=1400,y=900)


#registration frame for users to register to the application
class RegisterFrame(tk.Frame):

    def __init__(self, parent, controller):
        global fnameVar,lnameVar,emailVar,phoneVar, usernameVar,PINVar
        tk.Frame.__init__(self, parent)

        global register_list
        register_list = list()
        a = 500
        b = 700

        app_title = tk.Label(self, text="CryptoCurrency Predictions and Analysis System", font=LARGE_FONT)
        app_title.place(x=600, y=10, border='outside')

        label_title = tk.Label(self, text="MEMBER REGISTRATION", font=LARGE_FONT)
        label_title.place(x=600, y=100)

        label1 = tk.Label(self, text="First Name", font= LARGE_FONT)
        label1.place(x=a,y=250)
        fnameVar = tk.StringVar()
        fname = tk.Entry(self, textvariable=fnameVar, font= LARGE_FONT)
        fname.place(x=b,y=250)

        label2 = tk.Label(self, text="Last Name", font= LARGE_FONT)
        label2.place(x=a,y=300)
        lnameVar = tk.StringVar()
        lname = tk.Entry(self, textvariable=lnameVar, font= LARGE_FONT)
        lname.place(x=b,y=300)

        label3 = tk.Label(self, text="Email ", font= LARGE_FONT)
        label3.place(x=a, y=350)
        emailVar = tk.StringVar()
        email = tk.Entry(self, textvariable=emailVar, font= LARGE_FONT)
        email.place(x=b,y=350)

        label4 = tk.Label(self, text="Phone ", font= LARGE_FONT)
        label4.place(x=a, y=400)
        phoneVar = tk.StringVar()
        phone = tk.Entry(self, textvariable=phoneVar, font= LARGE_FONT)
        phone.place(x=b, y=400)

        label5 = tk.Label(self, text="Username ", font= LARGE_FONT)
        label5.place(x=a, y=450)
        usernameVar = tk.StringVar()
        username = tk.Entry(self, textvariable=usernameVar, font= LARGE_FONT)
        username.place(x=b, y=450)

        label6 = tk.Label(self, text="PIN ", font= LARGE_FONT)
        label6.place(x=a, y=500)
        PINVar = tk.StringVar()
        userpin = tk.Entry(self, textvariable=PINVar, font= LARGE_FONT,show = '*')
        userpin.place(x=b, y=500)

        btn1 = tk.Button(self, text=" Register ", command=register_user, font= LARGE_FONT)
        btn1.place(x=550, y=600)

        btn3 = tk.Button(self, text=" Goback ", command=lambda: controller.show_frame(LoginFrame), font= LARGE_FONT)
        btn3.place(x=750,y=600)



#Frame that presents the predicted CLOSE price and distributions of crypto currencies-
#bitcoin, ethereum and litecoin to the user
class DailyPredFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global yest_price_L, today_price_L, tomorrow_price_L, coinVar, trend_img_fig, predict_price_l
        global count_value_L,mean_value_L, STD_value_L, min_value_L, max_value_L, median_value_L
        global label_hist_image,label_pred_image

        app_title = tk.Label(self, text="CryptoCurrency Predictions and Analysis System", font=LARGE_FONT)
        app_title.place(x=600, y=10, border='outside')


        label_yest = tk.Label(self, text="Yesterday's Close Price ", font=MEDIUM_FONT)
        label_yest.place(x=490, y=150)
        yest_price_L = tk.Label(self, font=MEDIUM_FONT)
        yest_price_L.place(x=570, y=200)

        label_today = tk.Label(self, text="Today's Predicted Close Price", font=MEDIUM_FONT)
        label_today.place(x=910, y=150)
        today_price_L = tk.Label(self, font=MEDIUM_FONT)
        today_price_L.place(x=960, y=200)

        label_tomorrow = tk.Label(self, text="Tomorrow's Predicted Close Price", font=MEDIUM_FONT)
        label_tomorrow.place(x=1300, y=150)
        label_tomorrow.config(bg='yellow')
        tomorrow_price_L = tk.Label(self, font=MEDIUM_FONT)
        tomorrow_price_L.place(x=1370, y=200)
        tomorrow_price_L.config(bg='turquoise')

        label_date_price = tk.Label(self, text="Predicted Price for your date", font=MEDIUM_FONT)
        label_date_price.place(x=100, y=150)
        label_date_price.config(bg='yellow')
        predict_price_l = tk.Label(self, font=MEDIUM_FONT)
        predict_price_l.place(x=150, y=200)
        predict_price_l.config(bg='turquoise')

        label_pred_image = tk.Label(self, font=SMALL_FONT)
        label_pred_image.place_forget()

        label_hist_image = tk.Label(self, font=SMALL_FONT)
        label_hist_image.place_forget()

        label_clickme = tk.Label(self, text = "Wanna know this moment's price?", font=MEDIUM_FONT)
        label_clickme.place(x=400, y=300)
        btn_clickme = tk.Button(self, text=" click me ", command=show_current_price, font=MEDIUM_FONT)
        btn_clickme.place(x=750, y=300)
        btn_clickme.config(bg='SkyBlue2')

        label_stats_title = tk.Label(self, text = "Close Price Statistics", font=LARGE_FONT)
        label_stats_title.place(x=820,y=400)

        label_count = tk.Label(self, text="Count:", font=SMALL_FONT)
        label_count.place(x=850, y=500)
        count_value_L = tk.Label(self, font=SMALL_FONT)
        count_value_L.place(x=950, y=500)

        label_mean = tk.Label(self, text="Mean:", font=SMALL_FONT)
        label_mean.place(x=850, y=550)
        mean_value_L = tk.Label(self, font=SMALL_FONT)
        mean_value_L.place(x=950, y=550)

        label_STD = tk.Label(self, text="STD:", font=SMALL_FONT)
        label_STD.place(x=850, y=600)
        STD_value_L = tk.Label(self, font=SMALL_FONT)
        STD_value_L.place(x=950, y=600)

        label_min = tk.Label(self, text="Min:", font=SMALL_FONT)
        label_min.place(x=850, y=650)
        min_value_L = tk.Label(self, font=SMALL_FONT)
        min_value_L.place(x=950, y=650)

        label_max = tk.Label(self, text="Max:", font=SMALL_FONT)
        label_max.place(x=850, y=700)
        max_value_L = tk.Label(self, font=SMALL_FONT)
        max_value_L.place(x=950, y=700)

        label_median = tk.Label(self, text="Median:", font=SMALL_FONT)
        label_median.place(x=850, y=750)
        median_value_L = tk.Label(self, font=SMALL_FONT)
        median_value_L.place(x=950, y=750)

        btn2 = tk.Button(self, text=" Goback ", command=lambda: controller.show_frame(MenuFrame), font= LARGE_FONT)
        btn2.place(x=930, y=900)

        btn4 = tk.Button(self, text=" Logoff ", command=log_off, font=MEDIUM_FONT)
        btn4.place(x=1660, y=20)


#Frame that presents different features available in the application
class MenuFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        global predict_dateVar

        app_title = tk.Label(self, text="CryptoCurrency Predictions and Analysis System", font=LARGE_FONT)
        app_title.place(x=600, y=10, border='outside')


        label_title_l = tk.Label(self, text="PREDICT", font=LARGE_FONT)
        label_title_l.place(x=400, y=100)
        label_title_l.config(bg='yellow')

        label_title_r = tk.Label(self, text="VISUALIZE", font=LARGE_FONT)
        label_title_r.place(x=1300, y=100)
        label_title_r.config(bg='yellow')

        label_date_p = tk.Label(self, text="Enter a future date to predict price(MM/DD/YYYY)", font=MEDIUM_FONT)
        label_date_p.place(x=650, y=300)
        predict_dateVar = tk.StringVar()
        predict_date = tk.Entry(self, textvariable = predict_dateVar, font= LARGE_FONT)
        predict_date.place(x=1150, y=300)
        #predict_dateVar.set(today_date_fmt_default)

        pred_btn1 = tk.Button(self, text="  Predict and visualize Bitcoin Close Price   ", command=btc_predict_daily, font=LARGE_FONT)
        pred_btn1.place(x=250, y=500)
        pred_btn1.flash()

        pred_btn2 = tk.Button(self, text="  Predict and visualize Ethereum Close Price  ", command=eth_predict_daily, font= LARGE_FONT)
        pred_btn2.place(x=250, y=600)

        pred_btn3 = tk.Button(self, text="  Predict and visualize Litecoin Close Price  ", command=ltc_predict_daily, font=LARGE_FONT)
        pred_btn3.place(x=250, y=700)

        btn1 = tk.Button(self, text=" Visualize yearly distribution of close price of coins ",
                         command=lambda: controller.show_frame(ScatterPlotFrame),
                         font=LARGE_FONT)
        btn1.place(x=1100, y=500)
        btn1.flash()

        btn2 = tk.Button(self, text=" Visualize comparison of Volume and MarketCap of coins  ",
                         command=lambda: controller.show_frame(BarChartFrame),
                         font=LARGE_FONT)
        btn2.place(x=1100, y=600)

        btn3 = tk.Button(self, text=" Visualize Distribution of coins                        ",
                         command=lambda: controller.show_frame(BoxPlotFrame), font=LARGE_FONT)
        btn3.place(x=1100, y=700)

        btn4 = tk.Button(self, text=" Logoff ", command=log_off, font= MEDIUM_FONT)
        btn4.place(x=1680,y=20)



#Frame that provides options to generate scatter plots of yearly average close price of different crypto currencies
#Users have the option to choose whatever coin they wish to see the plot

class ScatterPlotFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global box_select,box_select_right, box_coins_list, box_sel_coins_list,label_image, tkimage

        box_sel_coins_list=[]

        app_title = tk.Label(self, text="CryptoCurrency Predictions and Analysis System", font=LARGE_FONT)
        app_title.place(x=600, y=10, border='outside')

        label_title = tk.Label(self, text="Yearly CLOSE price distribution ", font=LARGE_FONT)
        label_title.place(x=400, y=100)

        btn6 = tk.Button(self, text='IOTA', command=iota_view_scatter_plot, font=LARGE_FONT)
        btn6.place(x=250, y=200)

        btn1 = tk.Button(self,text = 'Bitcoin',command = bitcoin_view_scatter_plot,font=LARGE_FONT)
        btn1.place(x=250,y=300)

        btn2 = tk.Button(self, text = 'Ethereum', command = ethereum_view_scatter_plot,font = LARGE_FONT)
        btn2.place(x=250,y=400)

        btn3 = tk.Button(self, text='Ripple', command = ripple_view_scatter_plot,font = LARGE_FONT)
        btn3.place(x=250,y=500)

        btn4 = tk.Button(self, text='Ethereum Classic', command=etheclassic_view_scatter_plot, font=LARGE_FONT)
        btn4.place(x=250, y=600)

        btn5 = tk.Button(self, text='LiteCoin', command=litecoin_view_scatter_plot, font=LARGE_FONT)
        btn5.place(x=250, y=700)

        btn7 = tk.Button(self, text='Bitcoin Cash', command=bitcoincash_view_scatter_plot, font=LARGE_FONT)
        btn7.place(x=250, y=200)


        label_image = tk.Label(self, font=LARGE_FONT)
        label_image.place(x=800, y=300,width = 500, height = 300)
        label_image.place_forget()

        btn2g = tk.Button(self, text=" Goback ", command=lambda: controller.show_frame(MenuFrame), font=LARGE_FONT)
        btn2g.place(x=970, y=900)

        btn4l = tk.Button(self, text=" Logoff ", command=log_off, font=MEDIUM_FONT)
        btn4l.place(x=1680, y=20)


#Frame that provides options to generate box plots of HIGH price of differenct crypto currencies
#Users can choose one or more coins to visualize the difference in distribution of different coins
class BoxPlotFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global box_select,box_select_right, box_coins_list, box_sel_coins_list, label_box_image
        box_sel_coins_list=[]

        app_title = tk.Label(self, text="CryptoCurrency Predictions and Analysis System", font=LARGE_FONT)
        app_title.place(x=600, y=10, border='outside')

        label_title = tk.Label(self, text=" HIGH price distribution ", font=LARGE_FONT)
        label_title.place(x=400, y=100)

        scroll = tk.Scrollbar(self)
        scrollh = tk.Scrollbar(self)
        box_select = tk.Listbox(self, yscrollcommand=scroll.set, xscrollcommand=scrollh.set, height=15, width=30, font = SMALL_FONT, selectmode=tk.MULTIPLE)
        scroll.config(command=select.yview)
        box_select.place(x=200,y=200)

        label_box_image = tk.Label(self, font=LARGE_FONT)
        label_box_image.place(x=800, y=300, width=500, height=300)
        label_box_image.place_forget()

        box_select_right = tk.Listbox(self, yscrollcommand=scroll.set, xscrollcommand=scrollh.set, height=15, width=30, font=SMALL_FONT)
        box_select_right.place(x=700,y=200)

        box_select.delete(0, tk.END)
        box_select_right.delete(0, tk.END)
        box_sel_coins_list.clear()

        btn2 = tk.Button(self, text=" Goback ", command=lambda: controller.show_frame(MenuFrame), font=LARGE_FONT)
        btn2.place(x=900, y=900)

        btn4 = tk.Button(self, text=" Logoff ", command=log_off, font=MEDIUM_FONT)
        btn4.place(x=1680, y=20)

        btn_add = tk.Button(self,text="add>>", command = box_display_selected_items, font=LARGE_FONT)
        btn_add.place(x=540,y=300)

        btn_remove= tk.Button(self,text="<<remove", command = box_remove_selected_items, font=LARGE_FONT)
        btn_remove.place(x=540,y=380)

        btn_view_vchart = tk.Button(self,text ="View Box Plot", command = view_box_plot, font=LARGE_FONT)
        btn_view_vchart.place(x=500, y=600)

        box_coins_list = ["BTC-Bitcoin","ETH-Ethereum","XRP-Ripple","BTCH-BitCoinCash","XLM-Stellar",
                      "LTC-LiteCoin","NEO-Chinese Ethereum","IOTA-MIOTA","EOS-EOS"]

        box_coins_list.sort()

        for i in box_coins_list:
            box_select.insert(tk.END,i)


#Frame that provides a user with features to generate bar chart of volume and market cap of cryptocurrencies
#user can pick and visualize the distribution of different cryptocurrencies
class BarChartFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global select,select_right, coins_dictionary, label_select1, coins_list, sel_coins_list,label_bar_image
        sel_coins_list=[]

        app_title = tk.Label(self, text="CryptoCurrency Predictions and Analysis System", font=LARGE_FONT)
        app_title.place(x=600, y=10, border='outside')

        label_title = tk.Label(self, text=" Volume and MarketCap distribution ", font=LARGE_FONT)
        label_title.place(x=400, y=100)


        select = tk.Listbox(self,  height=20, width=30, font = SMALL_FONT, selectmode=tk.MULTIPLE)
        select.place(x=200,y=300)

        label_bar_image = tk.Label(self, font=SMALL_FONT)
        label_bar_image.place_forget()

        select_right = tk.Listbox(self, height=20, width=30, font=SMALL_FONT)
        select_right.place(x=700,y=300)

        select.delete(0, tk.END)
        select_right.delete(0, tk.END)
        sel_coins_list.clear()

        btn2 = tk.Button(self, text=" Goback ", command=lambda: controller.show_frame(MenuFrame), font=LARGE_FONT)
        btn2.place(x=750, y=900)

        btn4 = tk.Button(self, text=" Logoff ", command=log_off, font=MEDIUM_FONT)
        btn4.place(x=1680, y=20)

        btn_add = tk.Button(self,text="add>>", command = display_selected_items, font=LARGE_FONT)
        btn_add.place(x=550,y=400)

        btn_remove= tk.Button(self,text="<<remove", command = remove_selected_items, font=LARGE_FONT)
        btn_remove.place(x=550,y=600)

        btn_view_vchart = tk.Button(self,text ="View Volume Chart", command = view_volume_chart, font=LARGE_FONT)
        btn_view_vchart.place(x=350, y=800)

        btn_view_mchart = tk.Button(self, text="View Market Chart", command=view_market_chart, font=LARGE_FONT)
        btn_view_mchart.place(x=750, y=800)

        coins_list = ["BTC-Bitcoin","ETH-Ethereum","XRP-Ripple","BCH-BitCoinCash","XLM-Stellar",
                      "LTC-LiteCoin","ADA-Cardano","NEO-Chinese Ethereum","MIOTA-IOTA"]

        coins_list.sort()

        for i in coins_list:
            select.insert(tk.END,i)


#function to call scatter plot image generator for ripple
def ripple_view_scatter_plot():
    global scatter_fig, tkimage, img
    coin_type = 'ripple'
    scatter_plot_name = charts.scatter_plot(coin_type)
    scatter_fig = scatter_plot_name
    img = Image.open(scatter_fig)
    im_width = img.size[0]
    im_height = img.size[1]
    tkimage = ImageTk.PhotoImage(img)
    label_image['image'] = tkimage
    label_image.place(x=700, y=300, width=im_width, height=im_height)
    app.show_frame(ScatterPlotFrame)

#function to call scatter plot image generator for bitcoin
def bitcoin_view_scatter_plot():
    global scatter_fig, tkimage, img
    coin_type = 'bitcoin'
    scatter_plot_name = charts.scatter_plot(coin_type)
    scatter_fig = scatter_plot_name
    img = Image.open(scatter_fig)
    im_width = img.size[0]
    im_height = img.size[1]
    tkimage = ImageTk.PhotoImage(img)
    label_image['image'] = tkimage
    label_image.place(x=700, y=300, width=im_width, height=im_height)
    app.show_frame(ScatterPlotFrame)

#function to call scatter plot image generator for ethereum
def ethereum_view_scatter_plot():
    coin_type = 'ethereum'
    global scatter_fig, tkimage, img
    scatter_plot_name = charts.scatter_plot(coin_type)
    scatter_plot_show(scatter_plot_name)

#function to call scatter plot image generator for ethereum classic
def etheclassic_view_scatter_plot():
    coin_type = 'ethereumclassic'
    global scatter_fig, tkimage, img
    scatter_plot_name = charts.scatter_plot(coin_type)
    scatter_plot_show(scatter_plot_name)

#function to call scatter plot image generator for iota
def iota_view_scatter_plot():
    coin_type = 'iota'
    global scatter_fig, tkimage, img
    scatter_plot_name = charts.scatter_plot(coin_type)
    scatter_plot_show(scatter_plot_name)

#function to call scatter plot image generator for litecoin
def litecoin_view_scatter_plot():
    coin_type = 'litecoin'
    global scatter_fig, tkimage, img
    scatter_plot_name = charts.scatter_plot(coin_type)
    scatter_plot_show(scatter_plot_name)

#function to call scatter plot image generator for bitcoin cash
def bitcoincash_view_scatter_plot():
    coin_type = 'bitcoincash'
    global scatter_fig, tkimage, img
    scatter_plot_name = charts.scatter_plot(coin_type)
    scatter_plot_show(scatter_plot_name)


#function to read  and show the scatter plot image to the frame
def scatter_plot_show(scatter_plot_name):
    global scatter_fig, tkimage, img

    scatter_fig = scatter_plot_name
    img = Image.open(scatter_fig)
    im_width = img.size[0]
    im_height = img.size[1]
    tkimage = ImageTk.PhotoImage(img)
    label_image['image'] = tkimage
    label_image.place(x=700, y=300, width=im_width, height=im_height)
    app.show_frame(ScatterPlotFrame)

#function to invoke bar chart generator for volume of cryptocurrency
def view_volume_chart():
    global trend_fig,pred_img,im_width,im_height,tkimagepred
    c_type = "Volume"
    barplot_img_name_v = charts.bar_chart(sel_coins_list,c_type)
    trend_fig = barplot_img_name_v
    pred_img = Image.open(trend_fig)
    im_width = pred_img.size[0]
    im_height = pred_img.size[1]
    tkimagepred = ImageTk.PhotoImage(pred_img)
    label_bar_image['image'] = tkimagepred
    label_bar_image.place(x=1100, y=300, width=im_width, height=im_height)
    app.show_frame(BarChartFrame)

#function to invoke box plot generator for HIGH price of cryptocurrency
def view_box_plot():
    global trend_fig, pred_img, im_width, im_height, tkimagepred
    boxplot_img_name = charts.box_plot(box_sel_coins_list)
    trend_fig = boxplot_img_name
    pred_img = Image.open(trend_fig)
    im_width = pred_img.size[0]
    im_height = pred_img.size[1]
    tkimagepred = ImageTk.PhotoImage(pred_img)
    label_box_image['image'] = tkimagepred
    label_box_image.place(x=1100, y=200, width=im_width, height=im_height)
    app.show_frame(BoxPlotFrame)

#function to invoke bar chart generator for market cap of cryptocurrency
def view_market_chart():
    global trend_fig, pred_img, im_width, im_height, tkimagepred
    c_type = "Market"
    barplot_img_name_m = charts.bar_chart(sel_coins_list,c_type)
    trend_fig = barplot_img_name_m
    pred_img = Image.open(trend_fig)
    im_width = pred_img.size[0]
    im_height = pred_img.size[1]
    tkimagepred = ImageTk.PhotoImage(pred_img)
    label_bar_image['image'] = tkimagepred
    label_bar_image.place(x=1100, y=300, width=im_width, height=im_height)
    app.show_frame(BarChartFrame)

#function to display selected items in the listbox for charting
def box_display_selected_items():

    for add_item in box_select.curselection():
        box_select_right.insert(tk.END, box_coins_list[add_item])
        box_sel_coins_list.append(box_coins_list[add_item])

#function to remove selected items on clicking remove button
def box_remove_selected_items():
    for del_item in box_select_right.curselection():
        box_select_right.delete(del_item)
        box_sel_coins_list.remove(box_sel_coins_list[del_item])

#function to display selected items on the listbox
def display_selected_items():

    for add_item in select.curselection():
        select_right.insert(tk.END, coins_list[add_item])
        sel_coins_list.append(coins_list[add_item])

#function to remove selected items from listbox
def remove_selected_items():
    for del_item in select_right.curselection():
        select_right.delete(del_item)
        sel_coins_list.remove(sel_coins_list[del_item])

#function to close the application
def close_app():
    if messagebox.askokcancel(title='Bye', message="Are you sure to exit the app?") == 1:
        if messagebox.askokcancel(title='Bye', message="Have a great day!") == 1:

           os._exit(1)

#function to log off from the application
def log_off():
    if messagebox.askokcancel(title='Bye', message="Are you sure to log off?") == 1:

        app.show_frame(LoginFrame)

#Function to register a user into the system
def register_user():

    global fnameVar, lnameVar, emailVar, phoneVar, usernameVar, register_list

    if fnameVar.get().strip().__len__() == 0:
        messagebox.showinfo(title="Empty field warning",
                            message="Please enter first name!")
    elif lnameVar.get().strip().__len__() == 0:
        messagebox.showinfo(title="Empty field warning",
                            message="Please enter last name!")
    elif emailVar.get().strip().__len__() == 0:
        messagebox.showinfo(title="Empty field warning",
                            message="Please enter email")
    elif phoneVar.get().strip().__len__() == 0:
        messagebox.showinfo(title="Empty field warning",
                            message="Please enter phone")
    elif usernameVar.get().strip().__len__() == 0:
        messagebox.showinfo(title="Empty field warning",
                            message="Please enter username")
    elif str(PINVar.get()).strip().__len__() == 0:
        messagebox.showinfo(title="Empty field warning",
                            message="Please enter PIN")
    else:
        hashed_password = hashlib.sha512(str(PINVar.get()).encode('utf-8')).hexdigest()
        register_list.append(fnameVar.get())
        register_list.append(lnameVar.get())
        register_list.append(emailVar.get())
        register_list.append(phoneVar.get())
        register_list.append(usernameVar.get())
        register_list.append(hashed_password)
        fd.insert_into_table(register_list)
        messagebox.showinfo(title="Register", message="You are registered successfully!")
        app.show_frame(LoginFrame)

#function to login a user into the system
def login_user():


    if usernameloginVar.get().strip().__len__() == 0 :
        messagebox.showinfo(title="Empty field warning",
                            message="Please enter user name!")
    elif str(PINloginVar.get()).strip().__len__() == 0:
        messagebox.showinfo(title="Empty field warning",
                            message="Please enter password!")
    elif str(PINloginVar.get()).strip().__len__() > 0 and usernameloginVar.get().strip().__len__() > 0:
        hashed_password = hashlib.sha512(str(PINloginVar.get()).encode('utf-8')).hexdigest()
        if fd.check_username(usernameloginVar.get()):
            if fd.get_pin_to_match(usernameloginVar.get(),hashed_password):
                print("Login successful for the user")
                messagebox.showinfo(title="Login Success", message="You are successfully Logged in \n Please enter access code to access the application")
                labela.place(x=1200, y=500)
                access_code.place(x=1350, y=500)
                button3.place(x=1600, y=700)
            else:
                messagebox.showinfo(title="Invalid PIN", message="Please enter your correct PIN")
        else:
            messagebox.showinfo(title="No user", message="Username not found")

#function to validate the access code and PIN combination
def verify_access():

    with open("users.dat", "r") as access_file_read:
        access_invalid = True
        access_data = access_file_read.readline()
        while access_data.__len__() != 0 and access_invalid:
            a = access_data.split()
            file_pin = a[0]
            file_access_code = a[1]

            if file_pin == PINloginVar.get() and file_access_code == accessVar.get():
                print("Access verified for the user")
                messagebox.showinfo(title="Access",
                message="Your access is confirmed \n Welcome to our application")
                app.show_frame(MenuFrame)
                access_invalid = False

            access_data = access_file_read.readline()

    if access_invalid:
        messagebox.showinfo(title="Access code mismatch", message="Your access code doesn't match")

#function to show the current price by opening the respective web page for the coin
def show_current_price():

    global coin
    price_url = "https://coinmarketcap.com/currencies/"+coin+"/"
    webbrowser.open(price_url)

#function to invoke the future price prediction module for bitcoin.
#this function also formats the data to be presented to the console as well as to the frame
def btc_predict_daily():

    global trend_fig, hist_fig, hist_img, pred_img,tkimagepred, tkimagehist, predict_dateVar, coin
    coin = "bitcoin"

    if str(predict_dateVar.get()).strip().__len__() == 0:
        pass
    else:
        g_date_mm = str(predict_dateVar.get()).split('/')[0]
        g_date_dd = str(predict_dateVar.get()).split('/')[1]
        g_date_yyyy = str(predict_dateVar.get()).split('/')[2]

        today_date = dt.datetime(2018, int(date_mm), int(date_dd))
        g_date = dt.datetime(int(g_date_yyyy), int(g_date_mm), int(g_date_dd))

    if str(predict_dateVar.get()).strip().__len__() == 0:
        messagebox.showinfo(title="Blank date", message="Please enter the date you want to predict price for")
    elif g_date <= today_date:
        messagebox.showinfo(title="Future Date", message = "Please enter a future date for prediction")
    elif g_date > today_date:

        df, df_close_float_1, btc_price_yesterday, days_count, btc_summary_stats = prepare_data(coin,predict_dateVar.get())

        messagebox.showinfo(title="Wait", message="This takes time. Please wait!")

        btc_price_today,btc_price_tomorrow, prediction_that_date, btc_trend_img_name = btc_pred.btc_daily_pred_lstm(df_close_float_1, days_count)

        if days_count == 0:
            prediction_that_date = btc_price_today
        elif days_count == 1:
            prediction_that_date == btc_price_tomorrow

        messagebox.showinfo(title="Predicted Price", message="BTC price for tomorrow is: $ "+str(btc_price_tomorrow))
        yest_price_L['text'] = "$"+str(btc_price_yesterday)
        today_price_L['text'] = "$" + str(btc_price_today)
        tomorrow_price_L['text'] = "$"+str(btc_price_tomorrow)
        predict_price_l['text'] = "$"+str(prediction_that_date)

        print("--------------------- Bitcoin Close Price Summary Statistics--------------------")
        print(btc_summary_stats)
        print("--------------------- *************************************----------------------")

        count_value_L['text'] = str(round(btc_summary_stats[0],0))
        mean_value_L['text'] = "$"+str(round(btc_summary_stats[1],2))
        STD_value_L['text'] = "$"+str(round(btc_summary_stats[2],2))
        min_value_L['text'] = "$"+str(round(btc_summary_stats[3],2))
        max_value_L['text'] = "$"+str(round(btc_summary_stats[7],2))
        median_value_L['text'] = "$"+str(round(btc_summary_stats[5],2))

        hist_image_name = show_histogram(df,coin)

        trend_fig = btc_trend_img_name
        pred_img = Image.open(trend_fig)
        im_width = pred_img.size[0]
        im_height = pred_img.size[1]
        tkimagepred = ImageTk.PhotoImage(pred_img)
        label_pred_image['image'] = tkimagepred
        label_pred_image.place(x=1100, y=400, width=im_width, height=im_height)

        hist_fig = hist_image_name
        hist_img = Image.open(hist_fig)
        im_width = hist_img.size[0]
        im_height = hist_img.size[1]
        tkimagehist = ImageTk.PhotoImage(hist_img)
        label_hist_image['image'] = tkimagehist
        label_hist_image.place(x=100,y=400,width = im_width, height = im_height)
        app.show_frame(DailyPredFrame)


#function to invoke the future price prediction module for ethereum.
#this function also formats the data to be presented to the console as well as to the frame
def eth_predict_daily():

    global trend_fig, hist_fig, hist_img, pred_img, tkimagepred, tkimagehist, predict_dateVar, coin

    coin = "ethereum"

    if str(predict_dateVar.get()).strip().__len__() == 0:
        pass
    else:
        g_date_mm = str(predict_dateVar.get()).split('/')[0]
        g_date_dd = str(predict_dateVar.get()).split('/')[1]
        g_date_yyyy = str(predict_dateVar.get()).split('/')[2]

        today_date = dt.datetime(2018, int(date_mm), int(date_dd))
        g_date = dt.datetime(int(g_date_yyyy), int(g_date_mm), int(g_date_dd))

    if str(predict_dateVar.get()).strip().__len__() == 0:
        messagebox.showinfo(title="Blank date", message="Please enter the date you want to predict price for")
    elif g_date <= today_date:
        messagebox.showinfo(title="Future Date", message="Please enter a future date for prediction")
    elif g_date > today_date:

        df, df_close_float_1, eth_price_yesterday, days_count, eth_summary_stats = prepare_data(coin,predict_dateVar.get())

        messagebox.showinfo(title="Wait", message="This takes time. Please wait!")

        eth_price_today,eth_price_tomorrow,prediction_that_date, eth_trend_img = eth_pred.eth_daily_pred_lstm(df_close_float_1,days_count)

        if days_count == 0:
            prediction_that_date = eth_price_today
        elif days_count == 1:
            prediction_that_date = eth_price_tomorrow

        messagebox.showinfo(title="Predicted Price", message="ETH price for tomorrow is: $ "+str(eth_price_tomorrow))

        print("--------------------- Ethereum Close Price Summary Statistics--------------------")
        print(eth_summary_stats)
        print("--------------------- *************************************----------------------")

        tomorrow_price_L['text'] = "$"+str(eth_price_tomorrow)
        today_price_L['text'] = "$"+str(eth_price_today)
        yest_price_L['text'] = "$"+str(eth_price_yesterday)
        predict_price_l['text'] = "$"+str(prediction_that_date)

        count_value_L['text'] = str(round(eth_summary_stats[0], 0))
        mean_value_L['text'] = "$" + str(round(eth_summary_stats[1], 2))
        STD_value_L['text'] = "$" + str(round(eth_summary_stats[2], 2))
        min_value_L['text'] = "$" + str(round(eth_summary_stats[3], 2))
        max_value_L['text'] = "$" + str(round(eth_summary_stats[7], 2))
        median_value_L['text'] = "$" + str(round(eth_summary_stats[5], 2))

        eth_hist_img = show_histogram(df, coin)

        trend_fig = eth_trend_img
        pred_img = Image.open(trend_fig)
        im_width = pred_img.size[0]
        im_height = pred_img.size[1]
        tkimagepred = ImageTk.PhotoImage(pred_img)
        label_pred_image['image'] = tkimagepred
        label_pred_image.place(x=1100, y=400, width=im_width, height=im_height)

        hist_fig = eth_hist_img
        hist_img = Image.open(hist_fig)
        im_width = hist_img.size[0]
        im_height = hist_img.size[1]
        tkimagehist = ImageTk.PhotoImage(hist_img)
        label_hist_image['image'] = tkimagehist
        label_hist_image.place(x=100, y=400, width=im_width, height=im_height)
        app.show_frame(DailyPredFrame)


#function to invoke the future price prediction module for litecoin
#this function also formats the data to be presented to the console as well as to the frame
def ltc_predict_daily():

    global trend_fig, hist_fig, hist_img, pred_img, tkimagepred, tkimagehist, predict_dateVar, coin

    coin = "litecoin"
    if str(predict_dateVar.get()).strip().__len__() == 0:
        pass
    else:
        g_date_mm = str(predict_dateVar.get()).split('/')[0]
        g_date_dd = str(predict_dateVar.get()).split('/')[1]
        g_date_yyyy = str(predict_dateVar.get()).split('/')[2]

        today_date = dt.datetime(2018, int(date_mm), int(date_dd))
        g_date = dt.datetime(int(g_date_yyyy), int(g_date_mm), int(g_date_dd))

    if str(predict_dateVar.get()).strip().__len__() == 0:
        messagebox.showinfo(title="Blank date", message="Please enter the date you want to predict price for")
    elif g_date <= today_date:
        messagebox.showinfo(title="Future Date", message="Please enter a future date for prediction")
    elif g_date > today_date:
        df, df_close_float_1, ltc_price_yesterday,  days_count, ltc_summary_stats = prepare_data(coin,
                                                                                                         predict_dateVar.get())

        messagebox.showinfo(title="Wait", message="This takes time. Please wait!")

        ltc_price_today,ltc_price_tomorrow,prediction_that_date, ltc_trend_img = ltc_pred.ltc_daily_pred_lstm(df_close_float_1,days_count)

        if days_count == 0:
            prediction_that_date = ltc_price_today
        elif days_count == 1:
            prediction_that_date = ltc_price_tomorrow

        messagebox.showinfo(title="Predicted Price", message="LTC price for tomorrow is: $ "+str(ltc_price_tomorrow))

        print("--------------------- Litecoin Close Price Summary Statistics--------------------")
        print(ltc_summary_stats)
        print("--------------------- *************************************----------------------")

        tomorrow_price_L['text'] = "$"+str(ltc_price_tomorrow)
        today_price_L['text'] = "$"+str(ltc_price_today)
        yest_price_L['text'] = "$"+str(ltc_price_yesterday)
        predict_price_l['text'] = "$"+str(prediction_that_date)

        count_value_L['text'] = str(round(ltc_summary_stats[0], 0))
        mean_value_L['text'] = "$" + str(round(ltc_summary_stats[1], 2))
        STD_value_L['text'] = "$" + str(round(ltc_summary_stats[2], 2))
        min_value_L['text'] = "$" + str(round(ltc_summary_stats[3], 2))
        max_value_L['text'] = "$" + str(round(ltc_summary_stats[7], 2))
        median_value_L['text'] = "$" + str(round(ltc_summary_stats[5], 2))

        ltc_hist_img = show_histogram(df, coin)

        trend_fig = ltc_trend_img
        pred_img = Image.open(trend_fig)
        im_width = pred_img.size[0]
        im_height = pred_img.size[1]
        tkimagepred = ImageTk.PhotoImage(pred_img)
        label_pred_image['image'] = tkimagepred
        label_pred_image.place(x=1100, y=400, width=im_width, height=im_height)

        hist_fig = ltc_hist_img
        hist_img = Image.open(hist_fig)
        im_width = hist_img.size[0]
        im_height = hist_img.size[1]
        tkimagehist = ImageTk.PhotoImage(hist_img)
        label_hist_image['image'] = tkimagehist
        label_hist_image.place(x=100, y=400, width=im_width, height=im_height)
        app.show_frame(DailyPredFrame)
    else:
        messagebox.showinfo(title="Blank date", message="Please enter the date you want to predict price for")

#function to plot a histogram of the distribution of CLOSE price of different coins
def show_histogram(df, coin_type):
    plt.hist(df['Close**'],normed=1, facecolor='green', alpha=0.75)
    plt.xlabel("Close-Price")
    plt.ylabel("Frequency")
    plt.title("Histogram of "+coin_type.capitalize()+" close price")
    plt.grid(True)
    hist_img = coin_type.capitalize()+"histplot.png"
    plt.savefig(hist_img)
    plt.close()
    return hist_img

#function to prepare the data for feeding to the prediction model
#function uses in built html scrapping function to read the up-to-date price data from coinmarketcap.com
# for bitcoin, ethereum and litecoins. This html data is then read into a csv file which is later used
#for all predictions
def prepare_data(coin_name, predict_for_date):

    today_date = time.strftime("%x")
    date_mm = today_date.split("/")[0]
    date_dd = today_date.split("/")[1]
    today_date_fmt = "2018" + date_mm + date_dd


    s_date = date(2018, int(date_mm), int(date_dd))
    e_date = date(2018, int(predict_for_date.split('/')[0]), int(predict_for_date.split("/")[1]))
    diff = e_date - s_date
    no_of_days = int(str(diff).split()[0])
    print("days:", no_of_days)


 #   global df, yesterday_price, today_price
    url_1 = "https://coinmarketcap.com/currencies/"+coin_name+"/historical-data/?start=20130428&end"
    url_2 = "=" + today_date_fmt
    url = url_1 + url_2

    df_html, = pd.read_html(url)
    csv_file = coin_name+"-data.csv"
    df_html.to_csv(csv_file, index=False)

    df = pd.read_csv(csv_file, delimiter=',')


    close = df['Close**']
    yesterday_price = close[0]
    #today_price = close[0]

    df_sorted = df.iloc[::-1]

    df_sorted = df_sorted.drop(['Date', 'Open*', 'High', 'Low', 'Volume', 'Market Cap'], axis=1)

    # take the values of bit coin close column into a separate dataset

    df_close = df_sorted.values

    df_close_float = df_close.astype('float')  # converting all items in this df as float values

    #show_histogram(df,coin_name)

    return df, df_close_float, round(yesterday_price,2), no_of_days, close.describe()


app = PageController()


frame_width = 500
frame_height = 500

w = app.winfo_screenwidth()
h = app.winfo_height()

app.geometry("1800x1000")
app.title("CryptoCurrencies Prediction System")
app.mainloop()