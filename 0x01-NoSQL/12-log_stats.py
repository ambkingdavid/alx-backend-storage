#!/usr/bin/env python3
"""12-log_stats"""

from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient(host="localhost", port=27017)
    logs_collection = client.logs.nginx

    count_logs = logs_collection.count_documents({})
    print(f"{count_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count_method = logs_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count_method}")

    count_path = logs_collection.count_documents({"path": "/status"})
    print(f"{count_path} status check")
