#!/usr/bin/env python3
"""
This file contains a function to inserts a new doc in a collection
"""


def insert_school(mongo_collection, **kwargs):
    """
    kwargs: key word args
    mongo_collection: pymongo collection object
    return: the id of the added doc
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
