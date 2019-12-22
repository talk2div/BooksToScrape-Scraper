# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import requests

class BookstoscrapeSpider(CrawlSpider):
    name = 'bookstoscrape'
    allowed_domains = ['books.toscrape.com']

    #defining user-agent
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'


    def start_requests(self):
        yield scrapy.Request(url='http://books.toscrape.com',headers={
            'User-Agent':self.user_agent
        })


    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h3/a'), callback='parse_item', follow=True,process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a'),process_request='set_user_agent')
    )

    def set_user_agent(self,request):
        return request
    
    def parse_item(self, response):
        yield {
            'Book_Name': response.xpath('//h1/text()').get(),
            'Book_Price':response.xpath('//p[@class="price_color"]/text()').get(),
            'Instock':response.xpath('normalize-space(//p[@class="instock availability"]/text()[2])').get(),
            'Product Description':response.xpath('//div[@id="content_inner"]/article/p/text()').get(),
        }
    
