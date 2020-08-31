#Beau Heffron
#HW2
#HAIKU

#import libraries
import requests,json

#define string for reusing url's and list to hold words in haiku
orig_word = "https://api.datamuse.com/words?md=s&rel_trg="
nex_word = str("https://api.datamuse.com/words?md=s&lc=")
rhyme_ = str("&rel_rhy=")
words = []

def haiku(word):
    """Method to create haiku"""
    try:
        syn(word)
        next_word(words[0],1,2)
        next_word(words[1],2,3)
        next_word(words[2],3,2)
        rhyme(words[1],4)
        next_word(words[4],5,3)
        rhyme(words[4],6)
        if len(words) == 7:
            haiku_print()
        else:
            print("Sorry, a valid Haiku could not be generated.")
    except:
        print("Sorry, a valid Haiku could not be generated.")
        

def rhyme(word,pos):
    """Method to get rhyming word where word is the word prior and pos is the position you are in the haiku"""
    response = requests.get(nex_word + word + rhyme_ + words[1])
    if response:
        data = json.loads(response.text)
        for line in data:
            if(line["numSyllables"] == 2 and line["word"] not in words):
                words.insert(pos,str(line["word"]))
                break
                    
def syn(word):
    """Method to get a synonym for the user input"""
    response = requests.get(orig_word+word)
    if response:
        data = json.loads(response.text)
        for line in data:
            if(line["numSyllables"] == 3):
                words.insert(0,str(line["word"]))
                break

def next_word(word,pos,syl):
    """Method to get next word for haiku where word is prior word, pos is position in haiku, and syl is the number of syllables"""
    response = requests.get(nex_word+word)
    if response:
        data = json.loads(response.text)
        for line in data:
            if(line["numSyllables"] == syl):
                words.insert(pos,str(line["word"]))
                break
            
def haiku_print():
    """Print Haiku"""
    print()
    print(words[0],words[1])
    print(words[2],words[3],words[4])
    print(words[5],words[6],"\n")
      
#MAIN
print("Hello, welcome to the predictive text Haiku generator!")
cont = 'yes'
while cont.lower() == 'yes':
    words.clear()
    word = input("What would you like to see a Haiku about?")
    haiku(word)
    cont = input("Would you like to see another Haiku (yes/no)?")




