import numpy
from gensim.parsing import strip_non_alphanum, strip_multiple_whitespaces
from tweepy import OAuthHandler
from tweepy import Cursor
from tweepy import API
from tweepy import error
import pymongo
import accounts
from twitter_keys import *
from gensim.models import Word2Vec
from enum import Enum

class type(Enum):
    TWEET=0
    USER=1
    TEXT=1
    
#mongo_client = pymongo.MongoClient("localhost:27017")
#mydb = mongo_client["TweetsTFG"]
#mycol = mydb["tweets"]
model = Word2Vec.load('twitter87\\twitter87.model')
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth, wait_on_rate_limit=True)



def get_tweet(id):
    try:
        tweet = api.get_status(id)
        print(tweet)
    except error.TweepError:
        raise ValueError("El tweet ID no puede ser accedido o no existe")
    return (tweet.text,tweet.author.screen_name)
get_tweet(1325005705812717569)

def get_account(id):

    try:
        user = api.get_user(id)
    except error.TweepError:
        raise ValueError("El ID de usuario no puede ser accedido o no existe")
    return user

get_account(23)

def get_data(text):
    tipo,text=get_type(text)
    print(tipo,text)

    if tipo == type.USER:
        cuenta=get_account(text)

    else:
        raw_text=text, autor="Propio"
        if tipo== type.TWEET:
            raw_text,autor=get_tweet(text)


def get_type(text):
    #si hay mas de una palabra es raw text
    if len(text.split(" "))>1:
        return type.TEXT,text

    #dirreccion web completa
    if text.startswith("https://twitter.com/"):
        text=text.replace("https://","")
    #dirreccion twetter
    if text.startswith("twitter.com/"):
        text = text.replace("twitter.com/", "")
        aux=text.split("/")
        #es una cuenta
        if len(aux)==1:
            tipo = type.USER
            text="@"+text
        #es un tweet o algo que no toca y lanzaria error
        elif len(aux)==3:
            tipo = type.TWEET
            text= aux[2]
        else:
            raise ValueError("La dirreccion web introducida no pertenece ni a un usuario ni a un tweet")
    #es el nombre de una cuenta
    elif text.startswith("@"):
        tipo=type.USER
    #es un id de un tweet
    elif text.isnumeric():
        tipo=type.TWEET
    #es raw text
    else:
        tipo=type.TEXT
    return tipo,text


def calculate_word_emmbedding(text):
    text = strip_multiple_whitespaces(strip_non_alphanum(text.lower())).split(" ")
    result = numpy.zeros(300, dtype="float32")
    result.setflags(write=True)
    for word in text:
        if word in model.wv.vocab and word not in stopword:
            result.__iadd__(model.wv.get_vector(word))

    return result