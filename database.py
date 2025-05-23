from bson.objectid import ObjectId
from pymongo import MongoClient

class MongoManager:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["football_club"]  

    def insert(self, collection_name: str, data: dict):
        return self.db[collection_name].insert_one(data)

    def find(self, collection_name: str, query: dict = {}, sort=None, limit=None):
        cursor = self.db[collection_name].find(query)
        if sort:
            cursor = cursor.sort(sort)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    
    def find_one(self, collection_name: str, query: dict = {}, sort=None, limit=None):
        cursor = self.db[collection_name].find_one(query)
        if sort:
            cursor = cursor.sort(sort)
        if limit:
            cursor = cursor.limit(limit)
        return cursor

    def find_by_id(self, collection_name: str, item_id: str):
        return self.db[collection_name].find_one({"_id": ObjectId(item_id)})

    def update(self, collection_name: str, item_id: str, update_data: dict):
        return self.db[collection_name].update_one(
            {"_id": ObjectId(item_id)}, {"$set": update_data}
        )

    def delete(self, collection_name: str, item_id: str):
        return self.db[collection_name].delete_one({"_id": ObjectId(item_id)})

    def count(self, collection_name: str, query: dict = {}):
        return self.db[collection_name].count_documents(query)

    def clear_collection(self, collection_name: str):
        return self.db[collection_name].delete_many({})
