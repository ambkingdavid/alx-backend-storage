#!/usr/bin/env python3
"""9-insert_school"""

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs.

    :param mongo_collection: pymongo collection object
    :param kwargs: keyword arguments representing the fields and values of the document to insert
    :return: the new _id of the inserted document
    """
    result = mongo_collection.insert_one(kwargs)
    return result._id
