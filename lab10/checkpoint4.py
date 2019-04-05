from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient('localhost', 27017)

if __name__ == '__main__':
    defs = client.mongo_db_lab.definitions
    # find all
    for doc in defs.find():
        print(doc)
    # find one
    print(defs.find_one({"word": "Capitaland"}))
    # fetch by object id
    print(defs.find_one({"_id": ObjectId("56fe9e22bad6b23cde07b8ce")}))
    # insert a new record
    print(defs.insert({"word": "cat", "defintion": "A cuddly animal"}))

