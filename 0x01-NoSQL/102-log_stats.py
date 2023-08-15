#!/usr/bin/env python3

"""This module  lists nginx stats"""


from pymongo import MongoClient

if __name__ == "__main__":
    # Establish the connection
    client = MongoClient(host="localhost", port=27017)
    # Select the database
    db = client["logs"]
    # Select the collection
    collection = db.nginx
    total_logs = collection.count_documents({})
    print("{} logs".format(total_logs))
    status = collection.count_documents({"path": "/status"})
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")
    print(f"{status} status check")

    # Retrieve and print the top 10 most present IPs
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    print("IPs:")
    for i, ip in enumerate(top_ips, 1):
        print(f"\t{ip['ip']}: {ip['count']}")
