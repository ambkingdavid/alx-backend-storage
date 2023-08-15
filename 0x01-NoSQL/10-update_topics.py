#!/usr/bin/env python3
"""10-update_topic"""

def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name.

    :param mongo_collection: pymongo collection object
    :param name: the school name to update
    :param topics: the list of topics approached in the school
    """
    mongo_collection.update_one({"name": name}, {"$set": {"topics": topics}})
