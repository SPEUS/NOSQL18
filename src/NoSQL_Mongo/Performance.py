import timeit
from pymongo import MongoClient
import redis


# Connection Redis
redis = redis.StrictRedis(host='localhost', port=6379, db=0)
# Connection MongoDB
client = MongoClient()
db = client.nosql_database
plzDocument = db.plzData

def mongo_get_citystate_for_id(id):
    return plzDocument.find_one({"_id": id})

def redis_get_citystate_for_id(id):
    return redis.hmget(id, "city", "state")

def mongo_get_plz_for_city(city):
    return list(plzDocument.find({"city": city}))

print("Starte Performancetest Redis vs. MongoDB...")
print("Zugriff über Key bzw. ID mit _id=01001")
input()
print("Redis")
redisTimeOne = timeit.timeit("redis_get_citystate_for_id(\"01001\")", "from __main__ import redis_get_citystate_for_id", number=1)
print("Erster Aufruf: %.4f ms" % (redisTimeOne*1000))
redisTimeMany = timeit.timeit("redis_get_citystate_for_id(\"01001\")", "from __main__ import redis_get_citystate_for_id", number=10000)
print("Pro Aufruf: %.4f ms (Bei 10000 Aufrufen)" % (redisTimeMany/10))
input()
print("MongoDB")
mongoTimeOne = timeit.timeit("mongo_get_citystate_for_id(\"01001\")", "from __main__ import mongo_get_citystate_for_id", number=1)
print("Erster Aufruf: %.4f ms" % (mongoTimeOne*1000))
mongoTimeMany = timeit.timeit("mongo_get_citystate_for_id(\"01001\")", "from __main__ import mongo_get_citystate_for_id", number=10000)
print("Pro Aufruf: %.4f ms (Bei 10000 Aufrufen)" % (mongoTimeMany/10))
input()
print("Zugriff über Feld (keine ID) mit city=HAMBURG")
input()
print("MongoDB")
mongoTimeOne = timeit.timeit("mongo_get_plz_for_city(\"HAMBURG\")", "from __main__ import mongo_get_plz_for_city", number=1)
print("Erster Zugriff: %.4f ms" % (mongoTimeOne*1000))
mongoTimeMany = timeit.timeit("mongo_get_plz_for_city(\"HAMBURG\")", "from __main__ import mongo_get_plz_for_city", number=100)
print("Pro Aufruf: %.4f ms (Bei 100 Aufrufen)" % (mongoTimeMany*10))