#!/usr/bin/env python3
"""
Script that provides statistics about Nginx logs stored in MongoDB.
"""


from pymongo import MongoClient

def log_stats():
    """
    Provides statistics about Nginx logs stored in MongoDB.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    
    # Get the total number of logs
    total_logs = nginx_collection.count_documents({})
    
    # Get the count for each method (GET, POST, PUT, PATCH, DELETE)
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_stats = {method: nginx_collection.count_documents(
                   {"method": method}) for method in methods}
    
    # Get the count of logs where method is GET and path is /status
    status_check = nginx_collection.count_documents(
                   {"method": "GET", "path": "/status"})
    
    # Display the statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_stats[method]}")
    print(f"{status_check} status check")

if __name__ == "__main__":
    log_stats()
