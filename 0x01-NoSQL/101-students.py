#!/usr/bin/env python3
"""101-students"""

def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    :param mongo_collection: pymongo collection object
    :return: list of students sorted by average score
    """
    pipeline = [
        { "$unwind": "$topics" },
        {
            "$group": {
                "_id": "$_id",
                "name": { "$first": "$name" },
                "averageScore": { "$avg": "$topics.score" }
            }
        },
        { "$sort": { "averageScore": -1 } }
    ]
    
    students = list(mongo_collection.aggregate(pipeline))
    return students
