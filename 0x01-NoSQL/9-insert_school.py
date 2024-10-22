#!/usr/bin/env python3

"""  Insert a document """


def insert_school(mongo_collection, **kwargs):
    """  Insert a document """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
