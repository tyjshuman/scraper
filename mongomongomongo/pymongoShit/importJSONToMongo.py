import json
import sys
import pymongo
import glob
import fileinput
import os
from pymongo import MongoClient

def read(jsonFile):
	client = MongoClient('mongodb://localhost:27017/')
	db = client["texasTest4"]

	counter = 0
	with open(jsonFile, 'r') as f:
		haveGoodies = False
		for line in f:
			parsedJSONLine = json.loads(line)
			try:
				if db[jsonFile.split('.')[0].split('/')[1]].find({"email":parsedJSONLine["email"]}).count() == 0:
					haveGoodies = True
					db[jsonFile.split('.')[0].split('/')[1]].insert(parsedJSONLine)
					counter += 1
					print parsedJSONLine
			except pymongo.errors.DuplicateKeyError as dke:
				print "Duplicate Key Error: ", dke
			except ValueError as e:
				print "Value Error: ", e
			
			if 0 == counter % 100 and 0 != counter : print "Loaded line: ", counter
	f.close
	db.close

	if 0 == counter and haveGoodies: 
		print "No lines were loaded, something's fucked"
	else : 
		print "Loaded ",counter, " lines"

fileName = sys.argv[1]
print os.listdir(fileName)
for textFile in os.listdir(fileName):
	read(fileName+textFile)
