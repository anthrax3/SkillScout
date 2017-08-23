#-*- coding: utf-8 -*-
"""
Web scraper built using the Scrapy framework
@author: stephen schneider
"""
import os
import scrapy
import time
from scrapy.crawler import CrawlerProcess

#creates new directory to store any output data if folder is missing
output_dir = '/home/stephen/Desktop/jobdata_out'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class JobSpider(scrapy.Spider):
    from secret_settings import *
    name = 'indeeditis'
    #allowed_domains = ['www.indeed.com']
    #start_urls = 'whatever the api gives us i guesss'
    allowed_domains = ['https://www.yahoo.com']
    start_urls = ['https://www.yahoo.com']


    #counts and extracts document links from followed link :
    def parse(self, response):
        self.logger.info("Visited %s", response.url)
        print (response.url)

process = CrawlerProcess()
process.crawl(JobSpider)
process.start() 
