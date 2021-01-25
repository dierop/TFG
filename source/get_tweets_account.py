# API para Twitter: http://docs.tweepy.org/en/latest/
# MongoDB: tendrás que instalar mongodb, en linux: sudo apt-get install mongodb y
# la libreria de python para trabajar con bases de datos Mongo -> https://pymongo.readthedocs.io/en/stable/
# Te recomiendo https://robomongo.org/download (Robo 3T (formerly Robomongo)) para crear bases de datos, colecciones y visualizar los documentos añadidos a la base de datos #
from tweepy import OAuthHandler
from tweepy import Cursor
from tweepy import API
from tweepy import error
import pymongo
import accounts
from twitter_keys import *


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Instanciar cliente para Tweepy #
api = API(auth, wait_on_rate_limit=True)

# Conectar a la MongoDB (en el ejemplo está en localhost:27017 sin usuario ni contraseña) para almacenar los tweets #
# He creado en el ejemplo una base de datos "TFGTweets" y una coleccion dentro "tweets". Esto ya depende de como lo quieras organizar
# puedes dejarlo asi, crear una coleccion para cada usuario de Twitter, ... #
mongo_client = pymongo.MongoClient("localhost:27017")
mydb = mongo_client["TweetsTFG"]
mycol = mydb["tweets"]


n_tweets_per_user = 300

#for topic in accounts.get_all_accounts().keys():
for topic in ["Deportes"]:
    for name in ["atletismoSomos"]: #MeridiemGames]
    #for name in accounts.get_all_accounts()[topic]:
    #for name in []:
        # Iterar cada usuario de acount #
        # Informacion del usuario, por si es util para tu aplicacion #
        user = "@"+name
        try :
            hist = api.get_user(user)
        except error.TweepError as e:
            print(e)
            print(user)
            break
        print(user)
        # Iterar para cada tweet de user que devuelve la API.
        # Puede lanzar alguna excepcion por abuso de la API de Twitter, intenta controlar esto si falla) #
        for status in Cursor(api.user_timeline,
                         screen_name=user,
                         tweet_mode="extended",inlude_rts=False).items():

            # Cada status es un objeto de Tweepy con mucha informacion asociada,
            # revisa los atributos para ver que te interesa usar. Para el buscador
            # seguro que necesitaras el texto del tweet, que esta en full_text.
            # Anyway, deberias guardar primero los tweets completos en la MongoDB #

            # Cogemos el json del tweet para guardarlo en la Mongo #
            s = status._json

            # No procesamos retweets (si te interesa mantenerlos, quita esta comprobacion) #
            if "retweeted_status" in s:
                continue

            # Añadir a la Mongo, se crea un nuevo campo "_id" en el status porque Mongo indexa
            # por "_id" (en lugar de por "id" que es el identificador de los tweets segun tweepy),
            # así evitamos repetidos.

            s["_id"] = s["id"]

            # Le añadimos tambien el topic al tweet para usarlo luego en el buscador #
            s["topic"] = topic

            # Intentamos insertarlo en la Mongo #
            try:
                mycol.insert_one(s)
            except pymongo.errors.DuplicateKeyError:
                pass


