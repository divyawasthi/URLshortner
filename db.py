from pymongo import MongoClient 

uri = "mongodb+srv://ddtuser:ddt_password@ddtdb.qz0h58k.mongodb.net/?retryWrites=true&w=majority&appName=ddtdb"
client = MongoClient(uri)
db = client['ddtdb']
urls = db['urls']
