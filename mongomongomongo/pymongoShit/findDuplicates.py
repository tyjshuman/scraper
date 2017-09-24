import pymongo
from pymongo import MongoClient

#Load the database
mongo = MongoClient("mongodb://localhost:27017")
db = mongo["virtuance"]


def run() :
	incompleteEntries = 0
	allClients = db.clients.find()
	for client in allClients :
		#print client["phone"]
		incompleteEntries += validateClientInfo(client)
		print hasDuplicates(client)

	print "Total incomplete entries: ",incompleteEntries

def validateClientInfo(client) :
	if client["name"] == None or client["phone"] == None or client["email"] == None or client["address"] == None:
		print client
		return  1
	else : 
		return 0

def hasDuplicates(client) :
	#duplicateName  		= db.clients.count({"name":client["name"]})
	#duplicatePhone 		= db.clients.count({"phone":client["phone"]})
	duplicateEmail 		= db.clients.count({"email":client["email"]})
	#duplicateAddress	= db.clients.count({"address":client["address"]})
	return duplicateEmail

run()
