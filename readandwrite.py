# Kavitha Madhavaraj #
# Main File

#Create a cron job to run the script in specific schedules. - Later
from config import host,port,collection,dataDB
import scrape
import readRss
import time
import pymongo
from pymongo import MongoClient
from pymongo.errors import BulkWriteError 

connection = MongoClient(host,port)
db = connection[dataDB]
db[collection].ensure_index([('url' , pymongo.ASCENDING),('title' , pymongo.ASCENDING)])

def readAndWrite(listOfLinks,rssExists):
	bulk = db[collection].initialize_unordered_bulk_op()
	print "Scrapping Inititated......"
	for links in listOfLinks:
		print "Processing "+ links +"..."
		success = False
		while not success:
			if rssExists:
				result = readRss.aggregate(links, listOfLinks[links])
			else:
				result = scrape.do_scrape(links, listOfLinks[links])
			if result:
				success = True
				for record in result[links]:
					#print record["url"]
					#db[collection].update({"url":record["url"]}, {"$setOnInsert": record}, True)
					#db[collection].update({"title":record["title"]}, {"$setOnInsert": record}, True)
					bulk.find({"url":record["url"]}).upsert().update({'$set':record})
					bulk.find({"title":record["title"]}).upsert().update({'$set':record})
				try:
					print "Scrapping completed.. Writing to DB..."
					result = bulk.execute()
					bulk = db[collection].initialize_unordered_bulk_op()
				except BulkWriteError as bwe:
					print result
			else:
				print "Retrying...."
				time.sleep(5)
				continue
	print "Done !"

