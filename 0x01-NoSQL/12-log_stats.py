#!/usr/bin/env python3

"""  Log stats """

from pymongo import MongoClient

if __name__ == "__main__":
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx

    print(f"{len(list(logs.find()))} logs")
    print("Methods:")
    for method in methods:
        count = len(list(logs.find({"method": method})))
        print(f"\tmethod {method}: {count}")
    print(f"{len(list(
        logs.find({"method": "GET", "path": "/status"})))} status check")
