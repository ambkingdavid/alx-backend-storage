#!/usr/bin/env python3
"""8-all"""

def list_all(mongo_collection):
    """
    Lists all documents in a collection.

    :param mongo_collection: pymongo collection object
    :return: list of documents
    """
    documents = []
    for doc in mongo_collection.find():
        documents.append(doc)
    return documents
