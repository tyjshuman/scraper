import scrapy
import json

class VirtuanceSpider(scrapy.Spider):
	name = 'virtuance'
	def start_requests(self):
		urls = ['http://tours.virtuance.com/public/tour/search']
	
		for page in range(70, 81):
			print "Scraping page: " + str(page)
			page_url = urls[0]+"/WFNull/"+ str(page) +"|1000|"
			yield scrapy.Request(url=page_url, callback=self.parse)

	def parse(self, response):
		#Iterate through the listings on the page
		if response.css('title::text').extract_first() == "Tours hosted by tours.virtuance.com":
			for links in response.xpath('.//a[contains(@id,"viewBranded")]'):
				page_url = links.xpath('./@href').extract_first()
				yield scrapy.Request(url=page_url, callback=self.parse)
		else:
			#extract the contact information
			address = response.css('title::text').extract_first().split(" - ")[0]
			if(len(response.css('div[id=agentInfoInner]')) > 0):
				contact = response.css('div[id=agentInfoInner]')[0]
				name = contact.css('span[id=customerFullName]::text').extract_first()
       			  	company = contact.css('span[id=customerCompany]::text').extract_first()
		                phone = contact.css('span[id=customerContactPhone]::text').extract_first()
     	               		email = contact.css('a[id=customerEmail]::text').extract_first()
				if name is None:
					logging.log(logging.ERROR, "Missed name at: " + page_url)
				else:
					yield {
						'name' : name,
						'company' : company,
						'phone' : phone,
						'email' : email,
						'address' : address
					}
			else:
				jsonresponse = json.loads(response.body_as_unicode().split("      window.tourData = ")[1].split("\n    </script>")[0])
       		         	name = jsonresponse["tour"]["agents"][0]["name"]
       		         	company = jsonresponse["tour"]["agents"][0]["broker"]
               		 	phone = jsonresponse["tour"]["agents"][0]["phone"]
               		 	email = jsonresponse["tour"]["agents"][0]["email"]

                		yield{
                        		'name' : name,
                        		'company' : company,
                        		'phone' : phone,
                        		'email' : email,
                        		'address' : address
                       		 }
