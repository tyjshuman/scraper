import json
import pymongo
from pymongo import MongoClient

def read(jsonFile):
	client = MongoClient('mongodb://localhost:27017/')
	db = client["virtuance"]

	counter = 0
	with open(jsonFile, 'r') as f:
		for line in f:
			try:
				db["clients"].insert(json.loads(line))
				counter += 1
			except pymongo.errors.DuplicateKeyError as dke:
				print "Duplicate Key Error: ", dke
			except ValueError as e:
				print "Value Error: ", e
			
			if 0 == counter % 100 and 0 != counter : print "Loaded line: ", counter
	f.close
	db.close

	if 0 == counter : 
		print "No lines were loaded, something's fucked"
	else : 
		print "Loaded ",counter, " lines"

read("/home/tshuman/projects/scrapers/virtuance/virtuance_scraper/virtuance_scraper/scrapedPages/scrapedPages.json")

