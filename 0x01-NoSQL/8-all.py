#!/usr/bin/env python3
"""
This file contains a function that lists all documents in a collection
"""


def list_all(mongo_collection):
    """
    mongo_collection: pymongo collection object
    return : list of docs in the collection or empty list if no doc
    """
    documents = mongo_collection.find()
    return list(documents) if documents else []
