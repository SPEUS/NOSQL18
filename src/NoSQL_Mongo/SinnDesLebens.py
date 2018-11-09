from pymongo import MongoClient
import json
from functools import reduce
from datetime import date
import re

client = MongoClient()
db = client.nosql_database
sinnDesLebens = db.sinnDesLebens

def input_to_json_magic(input):
    replacements = [("db.fussball.insert(", ""), (");", ""), ("name", "\"name\""),
                    ("gruendung", "\"gruendung\""), ("farben", "\"farben\""),
                    ("Tabellenplatz", "\"Tabellenplatz\""), ("nike", "\"nike\""), ("'", "\""),
                    (", }", "}"), (", ]", "]"), (", weiss", ", \"weiss")]

    almostCleanInput = str(reduce(lambda input, replacement: input.replace(replacement[0], replacement[1]), replacements, input))

    extractedDateValues = list(map(lambda value: int(value), almostCleanInput.split("new Date(")[1].split(")")[0].split(",")))
    extractedDate = date(int(extractedDateValues[0]), extractedDateValues[1], extractedDateValues[2])

    cleanInput = re.sub(r"new Date\(.*\)", "\""+str(extractedDate)+"\"", almostCleanInput)

    return json.loads(cleanInput)

def save_to_db(JSONdataset):
    sinnDesLebens.insert_one(JSONdataset)

with open('sinndeslebens.txt') as sinnDesLebensFile:
    for rawdataset in sinnDesLebensFile:
        if rawdataset.startswith("db"):
            save_to_db(input_to_json_magic(rawdataset))
