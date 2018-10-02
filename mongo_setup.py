import scrape
import pymongo

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db

collection = db.mars_scrape

data = scrape.scrape()

collection.insert_one(data)