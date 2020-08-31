#Beau Heffron
#HW3
#MOVIE TOOL for reviews, background, wordcloud, etc

#import libraries
import requests,json
import matplotlib.pyplot as plt
import skimage.io,xmltodict,nltk,textblob,json
import wordcloud

#store Links and Key
api_call = "https://www.omdbapi.com/?r=xml&apikey=fe2e15f5&t="
url = "https://dgoldberg.sdsu.edu/515/imdb/movie.json"
key = "fe2e15f5"


#methods for user requests
def background(data):
    print("Year:",data["root"]['movie']["@year"])
    print("Rating:",data["root"]['movie']["@rated"])
    print("Runtime:",data["root"]['movie']["@runtime"])
    print("Genre:",data["root"]['movie']["@genre"])
    print("Actors:", data["root"]['movie']["@actors"])
    print("Plot:",data["root"]['movie']["@plot"])
def reception(data):
    print("Awards:",data["root"]['movie']["@awards"])
    print("Metascore:",data["root"]['movie']["@metascore"])
    print("IMDb rating:",data["root"]['movie']["@imdbRating"])
def poster(data):
    image = skimage.io.imread(data["root"]['movie']["@poster"])
    plt.imshow(image, interpolation = "bilinear")
    plt.axis("off")
    plt.show()
def wordc(data):
    r = requests.get(data)
    if r:
        data = json.loads(r.text)
        reviews = ""
        for review in data:
            reviews+=(review["Review text"])+" "
        cloud = wordcloud.WordCloud(max_words = 500, width = 1000, height = 1000, collocations = False)
        cloud.generate(reviews)
        plt.imshow(cloud, interpolation = "bilinear")
        plt.axis("off")
        plt.show()
    else:
        print("Wordcloud could not generate")
def sentiment(data):
    r = requests.get(data)
    if r:
        data = json.loads(r.text)
        reviews = ""
        for review in data:
            reviews+=(review["Review text"])+" "
    print("Average IMDb review polarity:",textblob.TextBlob(reviews).polarity)
    print("Average IMDb review subjectivity:",textblob.TextBlob(reviews).subjectivity)
#moving request and reviews loop out of these two methods would be more efficient


#welcome and itit
print("Welcome to the movie analytics tool!")
cont = 'yes'
contin = 'yes'


#main
while(cont.lower() == 'yes'):
    movie = input("What movie would you like to analyze?")
    response = requests.get(api_call+(movie.lower()))
    link = url.replace('movie',movie.lower())
    if response:
        try:
            data = xmltodict.parse(response.text)
            while(contin == 'yes'):
                method = str(textblob.TextBlob(input("What would you like to see (background/reception/poster/wordcloud/sentiment)?")).correct().lower())
                print()
                if(method in "background"):
                    background(data)
                elif(method in "reception"):
                    reception(data)
                elif(method in "poster"):
                    poster(data)
                elif(method in "wordcloud"):
                    wordc(link)
                elif(method in "sentiment"):
                    sentiment(link)
                else:
                    print("Sorry, the tool could not successfully load, or does not have the feature",method)
                print()
                contin = input("Would you like to further analyze this movie (yes/no)?")
        except:
            print("Sorry, the movie could not be found")
    else:
        print("ERROR: COULD NOT CONNECT")
    cont = input("Would you like to analyze another movie (yes/no)?")