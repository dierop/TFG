import pymongo
import accounts
from gensim.models import Word2Vec
import numpy
import scipy
from gensim.parsing.preprocessing import strip_non_alphanum, strip_multiple_whitespaces
import pathlib
import json
from sklearn.metrics import f1_score

mongo_client = pymongo.MongoClient("localhost:27017")
mydb = mongo_client["TweetsTFG"]
mycol = mydb["tweets"]
model = Word2Vec.load('twitter87\\twitter87.model')


# hot to acces documnet in topic
# for doc in cursor:
#    print(doc)


def get_tweets_number_data():
    print("Cuentas temas")
    for topic in accounts.get_accounts_temas().keys():
        print("topic:", topic, "tiene", len(accounts.get_accounts_temas()[topic]), "cuentas y",
              mycol.count_documents(
                  {"topic": topic, "user.screen_name": {"$in": accounts.get_accounts_temas()[topic]}}), "tweets")
        cursor = mycol.find({"topic": topic})
        for user in accounts.get_accounts_temas()[topic]:
            print(user, "tiene", mycol.count_documents({"topic": topic, "user.screen_name": user}), "tweets")
        print("")

    print("Cuentas test")
    for topic in accounts.get_accounts_tests().keys():
        print("topic:", topic, "tiene", len(accounts.get_accounts_tests()[topic]), "cuentas y",
              mycol.count_documents(
                  {"topic": topic, "user.screen_name": {"$in": accounts.get_accounts_tests()[topic]}}), "tweets")
        cursor = mycol.find({"topic": topic})
        for user in accounts.get_accounts_tests()[topic]:
            print(user, "tiene", mycol.count_documents({"topic": topic, "user.screen_name": user}), "tweets")
        print("")


#get_tweets_number_data()


def stopwords_to_list_of_lists():
    fdict = []
    for p in pathlib.Path('stop_words').iterdir():
        f = open(p, "r",encoding="utf-8")
        list_of_lists = []
        for line in f:
            stripped_line = line.strip().encode("utf-8").decode("utf-8")
            list_of_lists.append(stripped_line)
        fdict.append(list_of_lists)
        f.close()
    js = json.dumps(fdict, indent=4, sort_keys=True, ensure_ascii=False)
    f = open("stopwords_list.json", "w")
    f.write(js)
    f.close()


#stopwords_to_list_of_lists()

def get_account_wv(account, stopword):
    cursor = mycol.find({"user.screen_name": account}, projection=["user.screen_name", "full_text"])
    sol = numpy.zeros(300, dtype="float32")
    sol.setflags(write=True)
    for tweet in cursor:
        text = strip_multiple_whitespaces(strip_non_alphanum(tweet["full_text"].lower())).split(" ")
        result = numpy.zeros(300, dtype="float32")
        result.setflags(write=True)
        for word in text:
            if word in model.wv.vocab and word not in stopword:
                result.__iadd__(model.wv.get_vector(word))
            sol.__iadd__(result)
    return sol.__itruediv__(mycol.count_documents({"user.screen_name": account}))


def get_topic_wv(topic, stopword):
    cursor = mycol.find({"topic": topic, "user.screen_name": {"$in": accounts.get_accounts_temas()[topic]}},
                        projection=["user.screen_name", "full_text"])
    sol = numpy.zeros(300, dtype="float32")
    sol.setflags(write=True)
    for tweet in cursor:
        text = strip_multiple_whitespaces(strip_non_alphanum(tweet["full_text"].lower())).split(" ")
        result = numpy.zeros(300, dtype="float32")
        result.setflags(write=True)
        for word in text:
            if word in model.wv.vocab and word not in stopword:
                result.__iadd__(model.wv.get_vector(word))
        sol.__iadd__(result)
    return sol.__itruediv__(
        mycol.count_documents({"topic": topic, "user.screen_name": {"$in": accounts.get_accounts_temas()[topic]}}))


def topics_wv(stopword):

    dic = dict()
    for topic in accounts.get_accounts_tests().keys():
        total = get_topic_wv(topic, stopword)
        total.setflags(write=True)
        dic[topic] = total
        for user in accounts.get_accounts_tests()[topic]:
            total = get_account_wv(user, stopword)
            total.setflags(write=True)
            dic[user] = total
    print("macro_F1:")
    calculate_macro_f1(dic)
    print("Distancias:")
    view_distances(dic)



def view_distances(dic):
    accuraci = 0
    for topic in accounts.get_accounts_tests().keys():
        print("Cuentas de", topic, ":")
        for user in accounts.get_accounts_tests()[topic]:
            print("Distancias de", user, ":")
            best_result = 1
            theme = ""
            for tema in accounts.get_accounts_tests().keys():
                distance = scipy.spatial.distance.cosine(dic[tema], dic[user])
                print("\t", tema, "", distance)
                if distance < best_result:
                    theme = tema
                    best_result = distance
            if topic == theme:
                accuraci += 1
    print("\n", accuraci / 25 * 100)


def calculate_macro_f1(dic):
    distancias = numpy.zeros((25, 5),dtype=float)
    temas=[*accounts.get_accounts_tests().keys()]

    for ind_user in range(0,len(accounts.get_test_accounts_in_order())):
        for ind_tema in range(0, len(temas)):
            num1=dic[temas[ind_tema]]
            num2=dic[accounts.get_test_accounts_in_order()[ind_user]]
            distancias[ind_user,ind_tema]=scipy.spatial.distance.cosine(num1, num2)

    predict=numpy.argmin(distancias,axis=1)
    real=[num//accounts.get_length_one_test_theme() for num in range(0,len(accounts.get_test_accounts_in_order()))]
    result=f1_score(y_true=real,y_pred=predict,average="macro")
    print(result)

f = open("stopwords_list.json", "r")
stopword = json.load(f)
[topics_wv(stop) for stop in stopword]

# get_distances_with_divs()

# get_tweets_number_data()
