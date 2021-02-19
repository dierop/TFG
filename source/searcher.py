import json
import pickle

import numpy
from gensim.parsing import strip_non_alphanum, strip_multiple_whitespaces
from tweepy import OAuthHandler
from tweepy import Cursor
from tweepy import API
from tweepy import error
import pymongo
from twitter_keys import *
from gensim.models import Word2Vec
from enum import Enum


class type(Enum):
    TWEET = 0
    USER = 1
    TEXT = 2


class searcher():
    def __init__(self):
        mongo_client = pymongo.MongoClient("localhost:27017")
        mydb = mongo_client["TweetsTFG"]
        self.mycol = mydb["tweets"]
        self.model = Word2Vec.load('twitter87\\twitter87.model')
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = API(auth, wait_on_rate_limit=True)
        self.stopword = json.load(open("stopwords_list.json", "r"))[2]
        self.tweets_tree, self.tweets_dict = pickle.load(open("data/tweets_KDTree_dict.pickle", "rb"))
        self.users_tree, self.users_dict = pickle.load(open("data/user_KDTree_dict.pickle", "rb"))
        self.temas_tree, self.temas_dict = pickle.load(open("data/tema_KDTree_dict.pickle", "rb"))

    def get_tweet(self, id):
        try:
            tweet = self.api.get_status(id, tweet_mode='extended')
        except error.TweepError:
            raise ValueError("El tweet ID no puede ser accedido o no existe")
        return tweet.full_text, tweet.author.screen_name

    def account_exists(self, id):

        try:
            user = self.api.get_user(id)
        except error.TweepError:
            raise ValueError("El ID de usuario no puede ser accedido o no existe")
        return user

    def get_data(self, text):
        tipo, text = self.get_type(text)

        if tipo == type.USER:
            autor = text
            self.account_exists(text)
            raw_text = None
            embedding = self.get_account_word_emmbedding(text)

        else:
            if tipo == type.TWEET:
                raw_text, autor = self.get_tweet(text)
            else:
                raw_text = text
                autor = "Propio"
            embedding = self.calculate_word_emmbedding(raw_text)

        return tipo, raw_text, autor, embedding

    def get_type(self, text):
        # si hay mas de una palabra es raw text
        if len(text.split(" ")) > 1:
            return type.TEXT, text

        # dirreccion web completa
        if text.startswith("https://twitter.com/"):
            text = text.replace("https://", "")
        # dirreccion twitter
        if text.startswith("twitter.com/"):
            text = text.replace("twitter.com/", "")
            aux = text.split("/")
            # es una cuenta
            if len(aux) == 1:
                tipo = type.USER
                text = text
            # es un tweet o algo que no toca y lanzaria error
            elif len(aux) == 3:
                tipo = type.TWEET
                text = aux[2]
            else:
                raise ValueError("La dirreccion web introducida no pertenece ni a un usuario ni a un tweet")
        # es el nombre de una cuenta
        elif text.startswith("@"):
            tipo = type.USER
            text=text[1:]
        # es un id de un tweet
        elif text.isnumeric():
            tipo = type.TWEET
        # es raw text
        else:
            tipo = type.TEXT
        return tipo, text

    def get_account_word_emmbedding(self, account):
        result = numpy.zeros(300, dtype="float32")
        result.setflags(write=True)
        i = 0
        for status in Cursor(self.api.user_timeline,
                             screen_name=account,
                             tweet_mode="extended", inlude_rts=False).items(500):
            s = status._json
            result.__iadd__(self.calculate_word_emmbedding(s["full_text"]))
            i += 1
        return result.__itruediv__(i)

    def calculate_word_emmbedding(self, text):
        text = strip_multiple_whitespaces(strip_non_alphanum(text.lower())).split(" ")
        result = numpy.zeros(300, dtype="float32")
        result.setflags(write=True)
        for word in text:
            if word in self.model.wv.vocab and word not in self.stopword:
                result.__iadd__(self.model.wv.get_vector(word))

        return result

    def get_k_temas_vecinos(self, k, embedding):
        dist, ind = self.temas_tree.query(embedding.reshape(1, -1), k=k)
        return [self.temas_dict[i] for i in ind[0]], self.get_distancia_normalizada(dist[0])

    def get_k_cuentas_vecinos(self, k, embedding):
        dist, ind = self.users_tree.query(embedding.reshape(1, -1), k=k)
        return [self.users_dict[i] for i in ind[0]], self.get_distancia_normalizada(dist[0])

    def get_k_tweets_vecinos(self, k, embedding):
        dist, ind = self.tweets_tree.query(embedding.reshape(1, -1), k=k)
        return [self.tweets_dict[i] for i in ind[0]], self.get_distancia_normalizada(dist[0])

    def get_tweet_data(self, id):
        tweet = self.mycol.find_one({"id": id}, projection=["user.screen_name", "topic", "full_text"])
        return tweet["user"]["screen_name"], tweet["topic"], tweet["full_text"]

    def get_distancia_normalizada(self, distancias):
        # (x - x.min()) / (x.max() - x.min())
        return [round(((dis - distancias[0]) / (distancias[-1] - distancias[0]))*100)/100 for dis in distancias]


"""
prueba = searcher()
aux = prueba.get_data("https://twitter.com/MalditaTech/status/1353710544633655297")
print(aux[1],aux[2])
print(prueba.get_k_temas_vecinos(3,aux[3]))
print(prueba.get_k_cuentas_vecinos(3,aux[3]))
print(prueba.get_k_tweets_vecinos(3,aux[3]))

print(prueba.get_k_temas_vecinos(2,prueba.get_data("https://twitter.com/somosvivelibre/status/1353651377902333954")[3]))
print(prueba.get_k_temas_vecinos(2,))
print(prueba.get_k_temas_vecinos(2,prueba.get_data("1353331529070628864")[3]))

print(prueba.get_data("1354059133629161473"))
print(prueba.get_data("https://twitter.com/Kleo_cc"))
"""
