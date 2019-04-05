from pymongo import MongoClient
from datetime import datetime
client = MongoClient()


def random_word_requester():
    '''
    This function should return a random word and its definition and also
    log in the MongoDB database the timestamp that it was accessed.
    '''
    defs = client.mongo_db_lab.definitions
    word = list(defs.aggregate([{"$sample": { "size": 1 } }]))[0]
    defs.update(word, { "$push": { "dates": datetime.today() }})
    word = defs.find_one({"_id": word["_id"]})
    return word


if __name__ == '__main__':
    print(random_word_requester())
