import scrapy
import json
import logging

class VirtuanceSpider(scrapy.Spider):

	name = 'virtuance'
	site = ""	
	def start_requests(self):
	
		# eg. run on command line as: 
		# scrapy crawl virtuance -o output.json -a s=5 -a e=10 -a n=100
		start_page_number	= getattr(self, 's', '1') # using string numbers since command line args come in as strings.
		end_page_number		= getattr(self, 'e', '1')
		num_results_per_page	= getattr(self, 'n', '10')
		global site
		site			= getattr(self, 'h', 'virtuance')
	
		for page in range(int(start_page_number), int(end_page_number) + 1):
		
			page_url = "http://tours.%s.com/public/tour/search/WFNull/%s|%s|" % (site,page, num_results_per_page)
			logging.info("Scraping page: " + page_url)
			yield scrapy.Request(url=page_url, callback=self.parse)

	def parse(self, response):
	
		#Iterate through the listings on the page
		if response.css('title::text').extract_first() == "Tours hosted by tours.%s.com" % (site):
			for links in response.xpath('.//a[contains(@id,"viewBranded")]'):
				page_url = links.xpath('./@href').extract_first()
				yield scrapy.Request(url=page_url, callback=self.parse)
		else:
			#extract the contact information
			address = response.css('title::text').extract_first().split(" - ")[0]
			
			if(len(response.css('div[id=agentInfoInner]')) > 0):
			
				contact = response.css('div[id=agentInfoInner]')[0]
				name 	= contact.css('span[id=customerFullName]::text').extract_first()
				company = contact.css('span[id=customerCompany]::text').extract_first()
		        	phone 	= contact.css('span[id=customerContactPhone]::text').extract_first()
     	        		email 	= contact.css('a[id=customerEmail]::text').extract_first()
     	        
     	        		if name is None:
					logging.error("Missed name at: " + page_url)
					
				else:
					yield {
						'name' 		: name,
						'company' 	: company,
						'phone' 	: phone,
						'email' 	: email,
						'address' 	: address
					}
			else:
				jsonresponse = json.loads(response.body_as_unicode().split("      window.tourData = ")[1].split("\n    </script>")[0])
       		         	name 	= jsonresponse["tour"]["agents"][0]["name"]
       		         	company = jsonresponse["tour"]["agents"][0]["broker"]
               		 	phone 	= jsonresponse["tour"]["agents"][0]["phone"]
               		 	email 	= jsonresponse["tour"]["agents"][0]["email"]

                		yield{
                        		'name' : name,
                        		'company' : company,
                        		'phone' : phone,
                        		'email' : email,
                        		'address' : address
                       		 }
