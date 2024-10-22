#!/usr/bin/env python3
"""
This module contains a function that updates the topics of
a school document in a MongoDB collection based on the school name.
"""


def update_topics(mongo_collection, name, topics):
    """
    Updates the topics of a school document based on the school name.

    :param mongo_collection: pymongo collection object
    :param name: string representing the name of the school to update
    :param topics: list of strings representing the topics to update
    :return: None
    """
    mongo_collection.update_many(
        { "name": name },       # Find documents where the name matches
        { "$set": { "topics": topics } }  # Update the topics field
    )
