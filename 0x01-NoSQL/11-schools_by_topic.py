#!/usr/bin/env python3
"""
This module contains a function that finds and returns the list of schools
that have a specific topic in their topics field.
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools that have a specific topic.

    :param mongo_collection: pymongo collection object
    :param topic: string representing the topic to search for
    :return: list of schools that match the topic
    """
    return list(mongo_collection.find({"topics": topic}))
