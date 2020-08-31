#Beau Heffron
#5/5/2020
#Bitcoin trading bot
#utilizes machine learnings

import time,requests,json,matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import sklearn.neural_network
import sklearn.tree

#initiate variables for storage
Last_peak = 0
last_bottom = 0
last_price = 0
direction = 0
percent_change =0
time_since_last_trade = 0
prices = []
transactions = 0
buy_price = 0

methd = ""
usd = 0
btc = 0
#api url and parameters for live calls.
url = "https://bravenewcoin-v1.p.rapidapi.com/ticker"
querystring = {"show":"usd","coin":"btc"}
headers = {
    'x-rapidapi-host': "bravenewcoin-v1.p.rapidapi.com",
    'x-rapidapi-key': "a5f4e20305msh3b11ac011fe5a12p11ba4fjsne15f5e504cb7"
    }

#initiate machine learning

#last_bottom,last_price,direction
buyx=[[7600,7700,1],[3300,3350,1],
      [5000,4900,0],[5000,4800,1],
      [5500,5700,0],[9000,9050,1],
      [8800,9000,0]]
buyy=[1,1,0,0,0,1,1]

neural_buy = sklearn.neural_network.MLPClassifier()
neural_buy = neural_buy.fit(buyx, buyy)

buy_tree = sklearn.tree.DecisionTreeClassifier()
buy_tree = buy_tree.fit(buyx, buyy)
#change,last_peak,last_price,direction
sellx=[[5,9000,9000,1],[5,9000,8900,0],[4,5500,5700,1],
       [7,3300,3200,0],[6,3300,3200,1],[15,5000,5500,1],
       [15,5000,4900,0],[20,7000,6500,1],[20,7000,6500,0],
       [-1,3500,3200,0],[-4,6000,6500,0],[-20,6900,3000,0],
       [.10,1000,900,0],[.2,1000,9000,0],[.2,10000,9000,0]]
selly=[0,1,0,1,0,0,1,0,1,0,0,0,0,0,1]

neural_sell = sklearn.neural_network.MLPClassifier()
neural_sell = neural_sell.fit(sellx, selly)

sell_tree = sklearn.tree.DecisionTreeClassifier()
sell_tree = sell_tree.fit(sellx, selly)

def init():
    """Method to initiate variables and start simulation"""
    global last_price,last_bottom,last_peak,usd,methd
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response:
        data = json.loads(response.text)
        if(data["success"]):
            last_price = float(data["last_price"])
            price = ((float(data["price_24hr_pcnt"])/100)+1) * last_price
            prices.append(last_price)
            if(price<last_price):
                last_bottom = price
                last_peak = last_price
            else:
                last_bottom = last_price
                last_peak = price
            print("Current price of BTC in USD $",last_price)
            methd = CLM.get()
            usd = int(e1.get())
            root.destroy()
            run()
        else:
            print("Initiation failure please retry")
def run():
    """Method for running simmulation"""
    global last_price,last_bottom,last_peak,direction
    #2016*300 seconds = 1 week
    for x in range(0,2016):
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response:
            data = json.loads(response.text)
            if(data["success"]):
                if float(data["last_price"]) > last_price:
                    direction = 1
                else:
                    direction = 0
                last_price = float(data["last_price"])
                prices.append(last_price)
                if last_price > last_peak:
                    last_peak = last_price
                elif last_price < last_bottom:
                    last_bottom = last_price
                if(usd == 0):
                    change = (last_price-buy_price)/buy_price*100
                    a = [change,last_peak,last_price,direction]
                    if(methd == 'Neural Net'):
                        if(neural_sell.predict([a]) == 1):
                            conv("btc_to_usd")
                        else:
                            print("current_price $",last_price,"You Held your",btc)
                    elif(methd == 'Tree'):
                        if(sell_tree.predict([a]) == 1):
                            conv("btc_to_usd")
                        else:
                            print("current_price $",last_price,"You Held your",btc)
                    elif(methd == 'Method Beau'):
                        Beau_sell()
                else:
                    a = [[last_bottom,last_price,direction]]
                    if(methd == 'Neural Net'):
                        if(neural_buy.predict(a) == 1):
                            conv("usd_to_btc")
                        else:
                            print("You waited to buy with your $",usd)
                    elif(methd == 'Tree'):
                        if(buy_tree.predict(a) == 1):
                            conv("usd_to_btc")
                        else:
                            print("You waited to buy with your $",usd)
                    elif(methd =='Method Beau'):
                        Beau_buy()
                        
                time.sleep(300)  
            else:
                print("Unsuccessful call check credentials")
        else:
            print("API ERROR")

def conv(methd):
    """Method for converting bitcoin to usd and vice versa"""
    global usd,btc,buy_price
    if(methd == "btc_to_usd"):
        usd = btc*last_price
        btc = 0
        print("You sold your position and now have $",usd)
    else:
        btc = usd/last_price
        buy_price = last_price
        print("You bought",btc, "for $",usd)
        usd = 0 
       
def Beau_buy():
    """Criteria defined by me to buy bitcoin (have waited atlease 3 api calls, avg > last_price, and bitcoin has started increasing)"""
    print("Current Price:",last_price,", Session weighted avg:",sum(prices)/len(prices))
    if(len(prices)>=3 and sum(prices)/len(prices) > last_price and direction ==1):
        conv("usd_to_btc")
    else:
        print("You waited to buy with your $",usd)
def Beau_sell():
    """Criteria defined by me to sell bitcoin (last 3 prices sum to less<0, and buy price is greater than the current price)"""
    print("Current Price:",last_price,", Session weighted avg:",sum(prices)/len(prices))
    if((prices[-3]-prices[-2]-prices[-1])<0 and buy_price>last_price and direction == 0):
        conv("btc_to_usd")
    else:
        print("current_price $",last_price,"You Held your",btc)
     
     
     
     
#pulls btc prices from 2014 - present 
r = requests.get(url = "https://api.nomics.com/v1/currencies/sparkline?key=demo-26240835858194712a4f8cc0dc635c7a&ids=BTC,ETH,XRP&start=2014-01-01T00%3A00%3A00Z&end=2021-05-14T00%3A00%3A00Z")
d = json.loads(r.text)
r = []
q = []
for a in d:
    if a["currency"] == 'BTC':
        for n in a["prices"]:
            r.append(float(n))
        for y in a["timestamps"]:
            q.append(str(y)[0:10])


#plot 2014 - present bitcoin prices
plt.bar(q,r)
plt.xticks(rotation = 90, ha = "right")
plt.xlabel('Price')
graph = plt.gca()
graph.axes.xaxis.set_visible(False) #set to false because there are too many labels for most screen sizes
plt.ylabel("Date")
plt.title("Bitcoin in USD (2014-present)")
plt.show()     
     
       
#tkinter initiation  
root = tk.Tk()
root.title("Final Project")
label1 = tk.Label(root,text = "Pick Computer Learning Method             ")
label1.grid(column = 0,row = 0)
var = tk.StringVar()
CLM = ttk.Combobox(root,width = 30,textvariable = var)
CLM['values'] = ('Neural Net','Tree','Method Beau')
CLM.grid(column = 1,row = 0)
label2 = tk.Label(root,text = "Enter amount of starting capital(Integer) ")
label2.grid(column = 0,row = 1)
e1 = tk.Entry(root)
e1.grid(column = 1,row = 1)
b1 = tk.Button(root,text='Go',command = init)
b1.grid(column= 1,row=2)
root.mainloop()


