from email.mime import base
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import scrapy
import json

from TestScrapy.items import TestscrapyItem
    
class SpiderSpider(scrapy.Spider):
    a= 'a'
    name = 'spider'
    allowed_domains = ['foody.vn']
    start_urls = ['https://www.foody.vn/']
    base_url = 'https://www.foody.vn/'
    urls =["/can-tho","/ho-chi-minh","/ha-noi","/da-nang","/phu-quoc"]
    idx=1

    def parse(self, response):
        response_content = scrapy.Selector(response)
        item = TestscrapyItem()

        country_url = 'https://www.foody.vn/__get/Common/GetPopupLocation'

        headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
        "X-Requested-With": "XMLHttpRequest"
    }

        yield scrapy.Request(url = country_url, callback= self.parseCountry, headers= headers)
    
    def parseCountry(self, response):
        raw_data = response.body
        data = json.loads(raw_data)

        for a in data['AllLocations']:
            yield response.follow(url = self.base_url[:-1] + a['Url'], callback= self.parseCategory)



    def parseCategory(self, response):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
            "X-Requested-With": "XMLHttpRequest"
        }
        yield scrapy.Request(url ='https://www.foody.vn/common/_TopCategoryGroupMenu?isUseForSearch=false', callback= self.end, headers= headers, dont_filter= True)

    
    def end(self, response):
        response_content = scrapy.Selector(response)
        urls = response_content.xpath('//li[@data-id="1"]/ul[1]//li/a[1]/@href').extract()
        if urls:
            yield {str(self.idx): urls}



        

    
