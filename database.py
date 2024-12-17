import os
import pymongo
import sys
from urllib.parse import quote_plus


MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Url encode tu user and password

try:
    client = pymongo.MongoClient(MONGO_DETAILS)
    print(client.admin.command('ping'))
except pymongo.errors.ConfigurationError:
  print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
  sys.exit(1)


database = client["chatbot_db"]

users_collection = database.get_collection("users")
companies_collection = database.get_collection("companies")
products_collection = database.get_collection("products")
orders_collection = database.get_collection("orders")
clients_collection = database.get_collection("clients")

def get_db():
    db = client["chatbot_db"]
    try:
        yield db
    finally:
        client.close()