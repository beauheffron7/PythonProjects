#BEAU HEFFRON
##HW1 MIS515

import random, csv
def sim(x,y):
    q=0
    w=0
    r=0
    u=y
    for i in range(x):
        n = random.randint(-2000,2000)
        y*=(1+(n*.00001))
        if(n<0):
            q+=1
        elif(n>0):
            w+=1
        else:
            r+=1
    writer.writerow({"Initial price": u,"Number of days simulated":x,"Final price":y})
    print("After",x,"days,",y,"is the new stock price.")
    print("The stock price increased",w, "time(s), decreased",q,"time(s), and stayed the same",r,"time(s).")
with open('randomwalk.csv', 'w', newline='') as file:
    fields = ["Initial price","Number of days simulated","Final price"]
    writer = csv.DictWriter(file,fieldnames=fields)
    writer.writeheader()
    y="yes"    
    while(y == "yes"):
        price = float(input("What is the initial price of the stock?"))
        days = int(input("How many days would you like to simulate?"))
        sim(days,price)
        y = input("Would you like to perform another simulation(yes/no)?")
