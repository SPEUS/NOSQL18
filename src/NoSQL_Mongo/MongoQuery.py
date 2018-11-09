from easygui import *
from pymongo import MongoClient

client = MongoClient()
db = client.nosql_database
plzDocument = db.plzData

while 1:
    input = multenterbox("PLZ eingeben:", "Mongo Query", ["PLZ", "City"])
    if input is not None:
        if input[0]:
            result = plzDocument.find_one({"_id": input[0]})
            if result is not None:
                msgbox("City: " + result["city"] + " State: " + result["state"], "Mongo Query")
            else:
                msgbox("Kein Eintrag", "Mongo Query")
        elif input[1]:
            results = list(plzDocument.find({"city": input[1]}))
            if results is not None:
                msgbox("PLZ: " + ", ".join(map(lambda r: r["_id"], results)))
            else:
                msgbox("Kein Eintrag", "Mongo Query")
    else:
        break


