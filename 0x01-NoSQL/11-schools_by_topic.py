#!/usr/bin/env python3
"""11-schools_by_topic"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    :param mongo_collection: pymongo collection object
    :param topic: the topic searched
    :return: list of schools
    """
    schools = []
    for school in mongo_collection.find({"topics": topic}):
        schools.append(school)
    return schools
