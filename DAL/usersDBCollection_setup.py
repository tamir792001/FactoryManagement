from pymongo import MongoClient
import requests


client = MongoClient(port=27017)
db = client["factoryDB"]
users_collection = db["users"]

resp = requests.get('https://jsonplaceholder.typicode.com/users')
users_list = resp.json()
users_list = list(map(lambda x : {"userID" : x["id"], "fullname" : x["name"]},users_list))
for u in users_list:
    u["MaxActions"] = 20


users_collection.insert_many(users_list)