import pymongo
import csv
import re
from pymongo import MongoClient
#remove duplicates db.newClients.find({}, {email:1}).sort({_id:1}).forEach(function(doc){     db.newClients.remove({_id:{$gt:doc._id}, email:doc.email}); })

#Load the database
mongo = MongoClient("mongodb://localhost:27017")
db = mongo["virtuance"]
cursor = db.clients.find({},{'_id':0, 'name':1, 'company':1, 'email':1, 'address':1})

def validateClientInfo(client):
	valid = True
        if client["name"] == None or client["email"] == None or client["address"] == None or client["company"] == None:
                valid = False
		print "Entries incomplete"
	
	if not set(' ').intersection(client["name"]):
		valid = False	
		print "No space in name"

	if set('0123456789`~!@#$%^&*()_-+={[}]|\\:;"\'<,>.?/\u').intersection(client["name"]):
		valid = False
		print "Weird characters in name"

	if re.search('[0-9]{5},',client['address']) == None:
		valid = False
		print "No zip code"

	if re.search('the|resort|apartments|company|living|property|management|and|or',client['name'], re.IGNORECASE) != None:
		valid = False
		print "Name is a company name"

	if not valid:
		print client

	return valid

def writeCSV(entries):
	with open('allClients.csv','w') as outfile:
                fields = ['first','last','email','broker','zip']
                writer = csv.DictWriter(outfile, fieldnames=fields)
		for client in entries:
		        if validateClientInfo(client):
				try:
					firstName = client["name"][:client["name"].index(' ')]
					lastName = ""
					if client["name"].count(' ') is 1:
						lastName = client["name"][client["name"].index(' ') + 1:]
					elif client["name"].count(' ') is 2:
						lastName = client["name"][client["name"].rfind(' ') + 1:]
					writer.writerow({"first":firstName, "last":lastName, "email":client["email"], "broker":client["company"],"zip":re.search('[0-9]{5},',client['address']).group(0)[:-1]})
				except:
					print client

def run():
	writeCSV(cursor)

run()
