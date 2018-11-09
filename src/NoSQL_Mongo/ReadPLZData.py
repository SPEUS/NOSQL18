from pymongo import MongoClient
import json

client = MongoClient()
db = client.nosql_database
plzDocument = db.plzData

def convert_to_json(input):
    return json.loads(input.replace("\n", ""))

def save_to_db(JSONdataset):
    plzDocument.insert_one(JSONdataset)

with open('plz.data') as plzFile:
    for rawdataset in plzFile:
        save_to_db(convert_to_json(rawdataset))
