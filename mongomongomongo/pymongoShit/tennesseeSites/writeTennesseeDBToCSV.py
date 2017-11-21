import pymongo
import csv
import re
from pymongo import MongoClient
#remove duplicates db.newClients.find({}, {email:1}).sort({_id:1}).forEach(function(doc){     db.newClients.remove({_id:{$gt:doc._id}, email:doc.email}); })

#Load the database
mongo = MongoClient("mongodb://localhost:27017")
db = mongo["tennesseeSites"]

def validateClientInfo(client):
	valid = True
        if client["name"] == None or client["email"] == None or client["address"] == None:
                valid = False
		print "Entries incomplete"
	
	if not set(' ').intersection(client["name"]):
		valid = False	
		print "No space in name"

	if set('0123456789~!@#$%^*_+={[}]|:;\<>?').intersection(client["name"]):
		print set('0123456789~!@#$%^*_+={[}]|:;\<>?').intersection(client["name"])
		valid = False
		print "Weird characters in name"

#	if re.search('[0-9]{5},',client['address']) == None:
#		valid = False
#		print "No zip code"

	companyNameSearch = re.search('(\bthe\b)|(\bresort\b)|(\bapartments\b)|(\bcompany\b)|(\bliving\b)|(\bproperty\b)|(\bmanagement\b)|(\band\b)|(\bor\b)',client['name'], re.IGNORECASE)
	if companyNameSearch != None:
		print companyNameSearch.string[companyNameSearch.start():companyNameSearch.end()]
		valid = False
		print "Name is a company name"

	if not valid:
		print client

	return valid

def writeCSV(entries, collectionName):
	with open('csvs/'+collectionName+'.csv','w') as outfile:
                fields = ['first','last','email','broker','address','zip','state']
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
					try:
						zipCode = re.search('[0-9]{5},',client['address']).group(0)[:-1]
					except Exception as e:
						zipCode = None
						print e
						print "Could not get zip in nice format"
						print client
					if zipCode == None:
						try:
       		                                	zipCode = re.search('[0-9]{5}',client['address']).group(0)
                                     		except Exception as e:
                                                	zipCode = None
                                                	print e
                                                	print "Could not get any random zip"
							print client
					try:
						address = client["address"]
					except Exception as e:
						address = None
						print e
						print "Could not remove quotes from address"
						print client
					
					try:
                                                state = re.search('[A-Z]{2}',client["address"]).group(0)
                                        except Exception as e:
                                                state = None
                                                print e
                                                print "Could not find state code"
						print client
					writer.writerow({"first":firstName, "last":lastName, "email":client["email"], "broker":client["company"],"address":address,"zip":zipCode,"state":state})
				except Exception as e:
					print e
					print client

def run():
	collections = db.collection_names(include_system_collections=False)
	for collection in collections:
		cursor = db[collection].find({},{'_id':0, 'name':1, 'company':1, 'email':1, 'address':1})
		writeCSV(cursor,collection)

run()
