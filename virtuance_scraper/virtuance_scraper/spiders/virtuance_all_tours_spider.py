import scrapy
from scrapy.exceptions import CloseSpider

class VirtuanceSpider(scrapy.Spider):

	name 			= 'virtuance_all_tours'
	handle_httpstatus_list 	= [404]
	num_consecutive_404s 	= 0;
	consecutive_404_limit 	= 10;
	
	def start_requests(self):
		# eg. run on command line as: 
		# scrapy crawl virtuance_all_tours -o output.json -a s=5 -a e=10
		start_id	= getattr(self, 's', '1') # using string numbers since command line args come in as strings.
		end_id		= getattr(self, 'e', '10')

		for virtuance_customer_id in range(int(start_id), int(end_id) + 1):

			url = "http://tours.virtuance.com/public/vtour/customerTours/" + str(virtuance_customer_id)
			self.logger.info("Scraping page: " + url)
			request = scrapy.Request(url=url, callback=self.parse) 
			request.meta['virtuance_customer_id'] = virtuance_customer_id
			yield request
	

	def parse(self, response):
		virtuance_customer_id = response.meta['virtuance_customer_id']

		if response.status == 404:
            		self.num_consecutive_404s += 1
			self.logger.debug("[!] 404 for id: " + str(virtuance_customer_id) + ". Consectutive 404s: " + str(self.num_consecutive_404s))
            		if self.num_consecutive_404s >= self.consecutive_404_limit:
                		raise CloseSpider('Too many consecutive 404s. We may be at the end.')
				# raised at limit (10) but the threads will still take a while to wrap up.
				# eg. called at 10 but actually didn't stop until 26th 404
        	else:
            		self.num_consecutive_404s = 0

			if( len(response.css('div[id=agentInfoInner]')) == 0 ):
				self.logger.info("No agent info found for id: " + str(virtuance_customer_id))
			else: 
				contact 	= response.css('div[id=agentInfoInner]')[0]
				name 		= contact.css('span[id=customerFullName]::text').extract_first()
				company 	= contact.css('span[id=customerCompany]::text').extract_first()
				phone 		= contact.css('span[id=customerContactPhone]::text').extract_first()
				email 		= contact.css('a[id=customerEmail]::text').extract_first()
				website		= contact.css('a[id=customerWebSite]::text').extract_first()
				photo		= response.css('img[id=agentPhoto]').xpath('@src').extract_first()	
				properties 	= response.css('td[width="600"] a::text').extract()

				yield {
					'name'          	: name,
					'company'       	: company,
					'phone'         	: phone,
					'email'         	: email,
					'website'       	: website,
					'photo'			: photo,
					'virtuance_customer_id'	: virtuance_customer_id,
					'properties'		: properties
				}
