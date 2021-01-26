import json
import pickle
import pymongo
from sklearn.neighbors._kd_tree import KDTree
import accounts
from gensim.models import Word2Vec
import numpy
from gensim.parsing.preprocessing import strip_non_alphanum, strip_multiple_whitespaces

mongo_client = pymongo.MongoClient("localhost:27017")
mydb = mongo_client["TweetsTFG"]
mycol = mydb["tweets"]
model = Word2Vec.load('twitter87\\twitter87.model')


def get_wv_array_by_filter(filter, tweets_array, tweet_id_indice_dict):
    cursor = mycol.find(filter)
    sol = numpy.zeros(300, dtype="float32")
    sol.setflags(write=True)
    for tweet in cursor:
        sol.__iadd__(tweets_array[tweet_id_indice_dict[tweet["id"]]])
    return sol.__itruediv__(mycol.count_documents(filter))


def tweets_wv_info():
    f = open("stopwords_list.json", "r")
    stopword = json.load(f)[2]
    cursor = mycol.find()
    tweets_array = numpy.zeros((mycol.count_documents({}), 300), dtype="float32")
    tweets_array.setflags(write=True)
    ind_tweet_dict = {}
    tweet_id_indice_dict = {}
    i = 0
    for tweet in cursor:
        text = strip_multiple_whitespaces(strip_non_alphanum(tweet["full_text"].lower())).split(" ")
        for word in text:
            if word in model.wv.vocab and word not in stopword:
                tweets_array[i].__iadd__(model.wv.get_vector(word))

        ind_tweet_dict[i] = tweet["id"]
        tweet_id_indice_dict[tweet["id"]] = i
        i += 1

    return tweets_array, ind_tweet_dict, tweet_id_indice_dict


def save_KDTree_dict(array, dict, file):
    tree = KDTree(array)
    pickle.dump((tree, dict), open(file, "wb"), protocol=pickle.HIGHEST_PROTOCOL)


def indexer():
    tweets_array, ind_tweet_dict, tweet_id_indice_dict = tweets_wv_info()
    save_KDTree_dict(tweets_array, ind_tweet_dict, "data/tweets_KDTree_dict.pickle")
    topic_ind = 0
    user_ind = 0
    user_array = numpy.zeros((accounts.get_number_accounts(), 300), dtype="float32")
    topic_array = numpy.zeros((len(accounts.get_accounts_temas().keys()), 300), dtype="float32")
    user_dict = {}
    topic_dict = {}
    for topic in accounts.get_accounts_tests().keys():
        for user in accounts.get_all_accounts()[topic]:
            user_array[user_ind] = get_wv_array_by_filter({"user.screen_name": user}, tweets_array, tweet_id_indice_dict)
            user_dict[user_ind] = user
            user_ind += 1
        topic_array[topic_ind] = get_wv_array_by_filter(
            {"topic": topic, "user.screen_name": {"$in": accounts.get_accounts_temas()[topic]}}, tweets_array, tweet_id_indice_dict)
        topic_dict[topic_ind] = topic
        topic_ind += 1
    save_KDTree_dict(user_array, user_dict, "data/user_KDTree_dict.pickle")
    save_KDTree_dict(topic_array, topic_dict, "data/tema_KDTree_dict.pickle")


indexer()

