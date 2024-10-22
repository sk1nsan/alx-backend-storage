#!/usr/bin/env python3

"""  Log stats """

from pymongo import MongoClient


methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
client = MongoClient('mongodb://127.0.0.1:27017')
logs = client.logs.nginx

print(f"{logs.count()} logs")
print("Methods:")
for method in methods:
    count = logs.count({"method": method})
    print(f"\tmethod {method}: {count}")


print(f"{logs.count({"method": "GET", "path": "/status"})} status check")
