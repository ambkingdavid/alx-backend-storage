#!/usr/bin/env python3
"""101-students"""

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    :param mongo_collection: pymongo collection object
    :return: list of students sorted by average score
    """
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": {"_id": "$_id", "name": {"$first": "$name"}, "averageScore": {"$avg": "$scores.score"}}},
        {"$sort": {"averageScore": -1}}
    ]
    return list(mongo_collection.aggregate(pipeline))
