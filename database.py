from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["resume_screening"]

collection = db["results"]