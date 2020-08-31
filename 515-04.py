#Beau Heffron
#HW4
#3/28/2020
#TAKES IN SET JSON OF COMPANIES AND THEIR SUPPORT TWEETS AND RUN TEXT ANALYSIS

import requests,textblob,json,matplotlib.pyplot as plt,syllables,math
#sets for storing tweets
amazonhelp = []
AppleSupport = []
Ask_Spectrum = [] 
AskPlayStation = []
comcastcares = []
hulu_support = []
SpotifyCares = []
sprintcare = []
TMobileHelp = []
Uber_Support = []
UPSHelp = []
XboxSupport = []
#dataset to hold all the tweets, and set to hold all the @'s
datasets = [amazonhelp,AppleSupport,Ask_Spectrum,AskPlayStation,comcastcares,hulu_support,SpotifyCares,sprintcare,TMobileHelp,Uber_Support,UPSHelp,XboxSupport]
y = ["@amazonhelp","@AppleSupport","@Ask_Spectrum","@AskPlayStation","@comcastcares",
    "@hulu_support","@SpotifyCares","@sprintcare","@TMobileHelp","@Uber_Support","@UPSHelp","@XboxSupport"]

#method to call api and store the tweets
def init():
    response = requests.get("https://dgoldberg.sdsu.edu/515/customer_service_tweets_full.json")
    if response:
        data = json.loads(response.text)
        for company in data:
            if(company["Company"] == '@AmazonHelp'):
                amazonhelp.append(company["Text"])
            elif(company["Company"] == '@AppleSupport'):
                AppleSupport.append(company["Text"])
            elif(company["Company"] == '@Ask_Spectrum'):
                Ask_Spectrum.append(company["Text"])
            elif(company["Company"] == '@AskPlayStation'):
                AskPlayStation.append(company["Text"])
            elif(company["Company"] == '@comcastcares'):
                comcastcares.append(company["Text"])
            elif(company["Company"] == '@hulu_support'):
                hulu_support.append(company["Text"])
            elif(company["Company"] == '@SpotifyCares'):
                SpotifyCares.append(company["Text"])
            elif(company["Company"] == '@sprintcare'):
                sprintcare.append(company["Text"])
            elif(company["Company"] == '@TMobileHelp'):
                TMobileHelp.append(company["Text"])
            elif(company["Company"] == '@Uber_Support'):
                Uber_Support.append(company["Text"])
            elif(company["Company"] == '@UPSHelp'):
                UPSHelp.append(company["Text"])
            elif(company["Company"] == '@XboxSupport'):
                XboxSupport.append(company["Text"])
    else:
        print("API ERROR: RESTART PROGRAM AND TRY AGAIN")
#loop through all the tweets in every data set and find their avg polarity
def polarity():
    x = []
    for dataset in datasets:
        tweets = []
        for tweet in dataset:
            tweets.append(textblob.TextBlob(tweet).polarity)
        x.append(sum(tweets)/len(tweets))
    plt.bar(y,x)
    plt.xticks(rotation = 45, ha = "right")
    plt.xlabel('Twitter Handle')
    plt.ylabel('Polarity Level')
    plt.title('Polarity Level By Twitter Handle')
    plt.show()
    prntmethod(x)
#loop through all the tweets in every data set and find their avg Subjectivity
def subjectivity():
    x = []
    for dataset in datasets:
        tweets = []
        for tweet in dataset:
            tweets.append(textblob.TextBlob(tweet).subjectivity)
        x.append(sum(tweets)/len(tweets))
    plt.bar(y,x)
    plt.xticks(rotation = 45, ha = "right")
    plt.xlabel('Twitter Handle')
    plt.ylabel('Subjectivity Level')
    plt.title('Subjectivity Level By Twitter Handle')
    plt.show()
    prntmethod(x)
#method to print
def prntmethod(x):
    print()
    for i in range(0,12,1):
        print(y[i],':',x[i])
    print()
#method to loop through tweets and find avg smog or fkgl
def readability():
    m = input("Would you like to analyze FKGL or SMOG?")
    x = []
    if(m.lower() == 'fkgl'):
        for dataset in datasets:
            tweets = []
            for tweet in dataset:
                words = 0
                sentences = 0
                syl = 0
                blob = textblob.TextBlob(tweet)
                for sentence in blob.sentences:
                    sentences+=1
                    for word in sentence.words:
                        words+=1
                        syl +=  syllables.estimate(word)
                tweets.append((0.39*(words/sentences) + 11.8*(syl/words))-15.59)
            x.append(sum(tweets)/len(tweets))
        plt.bar(y,x)
        plt.xticks(rotation = 45, ha = "right")
        plt.xlabel('Twitter Handle')
        plt.ylabel('Flesch-Kincaid Grade Level')
        plt.title('Flesch-Kincaid Grade Level By Twitter Handle')
        plt.show()
        prntmethod(x)
    elif(m.lower() == 'smog'):
        for dataset in datasets:
            tweets = []
            for tweet in dataset:
                sent = 0
                polysyl = 0
                blob = textblob.TextBlob(tweet)
                for sentence in blob.sentences:
                    sent+=1
                    for word in sentence.words:
                        if(syllables.estimate(word)>=3):
                            polysyl+=1
                tweets.append((1.043*math.sqrt(polysyl*30/sent))+3.1291)
            x.append(sum(tweets)/len(tweets))
        plt.bar(y,x)
        plt.xticks(rotation = 45, ha = "right")
        plt.xlabel('Twitter Handle')
        plt.ylabel('SMOG Level')
        plt.title('SMOG Level By Twitter Handle')
        plt.show()
        prntmethod(x) 
    else:
        print("Sorry, that type of analysis is not supported. Please try again.")
#loop through all tweets and find avg formality
def formality():
    x = []
    for dataset in datasets:
        tweets = []
        for tweet in dataset:
            f=0
            c=0
            blob = textblob.TextBlob(tweet)
            for word,tag in blob.tags:
                if(tag in("NN","JJ","IN","DT")):
                    f+=1
                elif(tag in("PR","VB","RB","UH")):
                    c+=1
            if(f+c == 0 or f-c ==0):
                tweets.append(50)
            else:
                tweets.append(50*(((f-c)/(f+c))+1))
        x.append(sum(tweets)/len(tweets))
    plt.bar(y,x)
    plt.xticks(rotation = 45, ha = "right")
    plt.xlabel('Twitter Handle')
    plt.ylabel('Formality')
    plt.title('Formality By Twitter Handle')
    plt.show()
    prntmethod(x)
#search method to find stats on single company
def search(dataset):
    tweets_pol = []
    tweets_sub = []
    tweets_fkgl = []
    tweets_smog = []
    tweets_form = []
    for tweet in dataset:
        ws = 0
        sent = 0
        syl = 0
        f=0
        c=0
        polysyl = 0
        blob = textblob.TextBlob(tweet)
        tweets_pol.append(blob.polarity)
        tweets_sub.append(blob.subjectivity)
        for sentence in blob.sentences:
            sent+=1
            for word in sentence.words:
                syl+=syllables.estimate(word)
                ws+=1
                if(syllables.estimate(word)>=3):
                    polysyl+=1
        for word,tag in blob.tags:
            if(tag in("NN","JJ","IN","DT")):
                f+=1
            elif(tag in("PR","VB","RB","UH")):
                c+=1
        tweets_smog.append((1.043*math.sqrt(polysyl*30/sent))+3.1291)
        tweets_fkgl.append((0.39*(ws/sent) + 11.8*(syl/ws))-15.59)
        if(f+c == 0 or f-c ==0):
            tweets_form.append(50)
        else:
            tweets_form.append(50*(((f-c)/(f+c))+1))
    x = [sum(tweets_pol)/len(tweets_pol)
         ,sum(tweets_sub)/len(tweets_sub)
         ,sum(tweets_smog)/len(tweets_smog)
         ,sum(tweets_fkgl)/len(tweets_fkgl)
         ,sum(tweets_form)/len(tweets_form)
         ]
    print()
    print("Average polarity:",x[0])
    print("Average subjectivity:",x[1]) 
    print("Average Flesch-Kincaid Grade Level:",x[3])
    print("Average SMOG index:",x[2] )
    print("Average Formality index:",x[4])
    print()
#welcome message and initiation calls
print("Welcome to the customer service linguistics analyzer!\n")
init()
cont = 'yes'
#main
while cont == 'yes':
    methd = input("Which analysis would you like to perform (polarity/subjectivity/readability/formality/search)?")
    if methd.lower() == 'polarity':
        polarity()
    elif methd.lower() == 'subjectivity':
        subjectivity()
    elif methd.lower() == 'readability':
        readability()
    elif methd.lower() == 'formality':
        formality()
    elif methd.lower() == 'search':
        twit = input('Which Twitter handle would you like to search?')
        x=0
        for handle in y:
            if(handle.lower()==twit.lower()):
                search(datasets[x])
                break
            x+=1
        if(x==12):
            print("Sorry, that Twitter handle was not found. Please try again.")
    else:
        print("Sorry, that type of analysis is not supported. Please try again.")
    cont = input("Would you like to run another analysis (yes/no)?").lower()

# NOTES TO SELF
    # SEARCH repeats lines from other methods, could make all methods take another attribute so they can loop through all or just one
    #FOR MAKING THIS DATASET AGNOSTIC (company)
        #In init take company and remove @ symble and create a list with that name
        #append that list to datasets lists
        #loop through
