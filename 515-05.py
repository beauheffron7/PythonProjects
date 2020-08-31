#Beau Heffron
#HW5
#4/19/2020
#TAKES IN SET JSON OF COVID STATS BY STATE BY DATE AND RETURNS A GRAPH

import requests,json,matplotlib.pyplot as plt,itertools

StateDict = [
'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA',
'KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT',
'VA','WA','WV','WI','WY','DC']
#includes DC

#list of methods
methd = ['positive','death','totaltestresults','positiveincrease','negative','pending','hospitalizedcurrently',
         'hospitalizedcumulative','inicucurrently','inicucumulative','onventilatorcurrently','onventilatorcumulative',
         'recovered','hospitalized','total','posneg','deathincrease','hospitalizedincrease','negativeincrease','totaltestresultsincrease']
    
def step(a):
    """method for user input"""
    b = input("Which statistic would you like to search?")
    if(b.lower()in methd):
        c = input("Would you like to add a start date (yes/no)?")
        if(c.lower() == 'yes'):
            start = int(input("Which start date would you like to use (YYYYMMDD)?"))
        else:
            start = 'n'
        d = input("Would you like to add an end date (yes/no)?")
        if(d.lower() == 'yes'):
            end = int(input("Which end date would you like to use (YYYYMMDD)?"))
        else:
            end = 'n'
        method(a,b,start,end)
    else:
        print("INvalid Statisitic")
        
def method(a,b,c,d):
    """method to loop through and display the data that the user requested in step()"""
    response = requests.get("https://covidtracking.com/api/v1/states/daily.json")
    if response:
        data = json.loads(response.text)
        if(b.lower() == 'positiveincrease'):
            b = 'positiveIncrease'
        elif(b.lower() == 'totaltestresults'):
            b = 'totalTestResults'
        elif(b.lower() == 'hospitalizedcurrently'):
            b = 'hospitalizedCurrently'
        elif(b.lower()== 'hospitalizedcumulative'):
            b = 'hospitalizedCumulative'
        elif(b.lower()=='inicucurrently'):
            b = 'inIcuCurrently'
        elif(b.lower()=='inicucumulative'):
            b = 'inIcuCumulative'
        elif(b.lower()=='onventilatorcurrently'):
            b = 'onVentilatorCurrently'
        elif(b.lower()=='onventilatorcumulative'):
            b = 'onVentilatorCumulative'
        elif(b.lower()=='posneg'):
            b = 'posNeg'
        elif(b.lower()=='deathincrease'):
            b = 'deathIncrease'
        elif(b.lower()=='hospitalizedincrease'):
            b = 'hospitalizedIncrease'
        elif(b.lower()=='negativeincrease'):
            b = 'negativeIncrease'
        elif(b.lower()=='totaltestresultsincrease'):
            b = 'totalTestResultsIncrease'
        e = []
        f = []
        mi = 999999999
        ma = 0
        for record in data:
            if(record['state']==a.upper()):
                if(record['date']>ma):
                    ma = record['date']
                if(record['date']<mi):
                    mi = record['date']
        if c == 'n':
            c = mi
        if(d == 'n'):
            d = ma
        for record in data:
            if(record['state']==a.upper()):
                if(int(record["date"])>=c and int(record["date"])<=d):
                    e.append(str(record['date']))
                    if(str(record.get(b,0))=='None' or str(record.get(b,0))== 'null'):
                        f.append(0)
                    else:
                        f.append(record.get(b,0))
        print()
        z = "Coronavirus in "+a.upper()+" between "+str(c)+" and "+str(d)+" : "+b
        print(z,'\n')
        print('Date','\t'+b)
        for q,r in zip(e,f):
            print(q,r)
        plt.bar(e,f)
        plt.xticks(rotation = 90, ha = "right")
        plt.xlabel('Date')
        plt.ylabel(b)
        plt.title(z)
        plt.show()
    else:
        print("Failed to connect to API Please restart program")

#MAIN

print("Welcome to the coronavirus (COVID-19) live data analyzer!")
cont = 'yes'
while cont.lower() == 'yes':
    state = input('Which location would you like to search?')
    if(state.upper() in StateDict):
        step(state)
    else:
        print("Invalid State")
    cont = input('Perform another analysis (yes/no)?')
       
#if i used .lower() on the dataset it would reduce the amount of lines dramatically
    #can autopopulate methods list from the dataset itself if aswell to make the program usable even if the api add more parameters