#-*- coding: utf-8 -*-
"""
Web scraper built using the Scrapy framework
@author: stephen schneider
"""
import os
import scrapy
import time
import sys
import datetime
# enter working directory: os.chdir('/home/stephen/Code/Python/venv/SkillScout/backend')
# Add directory to path: sys.path.append('/home/stephen/Code/Python/venv/SkillScout/backend')

from scrapy.crawler import CrawlerProcess

#creates new directory to store any output data if folder is missing
#output_dir = '/home/stephen/Desktop/jobdata_out'
#if not os.path.exists(output_dir):
#   os.makedirs(output_dir)
     

class JobSpider(scrapy.Spider):
   from secret_settings import *
   name = 'jobspider'
   allowed_domains = ['www.indeed.com']
    
   #Ask for user input
    
   #user_city = raw_input("Enter city:\n")
   user_city = 'Boston'
   city_name = user_city.replace(" ", "+")
   #state_name = raw_input("Enter state abbreviation:\n")
   state_name = 'MA'
   start_urls = ['https://www.indeed.com/jobs?q=&l=' + city_name + '%2C+' + state_name + '&sort=date']
      
   #counts and extracts document links from followed link :
   def parse(self, response):
       from jobfunctions import scrape_link
       scrape_date = datetime.date.today().strftime("%m-%d-%Y")
       main_table = '/html/body/table[2]/tr/td/table/tr/td[2]'
       #Check if first link is non-sponsored..
       first_link = response.xpath(main_table + '/div[4]').extract_first()
       if first_link[14:25] == u'row  result':
          page_data = scrape_link(main_table, scrape_date, 4, response)
       else:
          first_link = response.xpath(main_table + '/div[5]').extract_first()
          if first_link[14:25] == u'row  result':
             page_data = scrape_link(main_table, scrape_date, 5, response)
          else:
             first_link = response.xpath(main_table + '/div[6]').extract_first()
             page_data = scrape_link(main_table, scrape_date, 6, response)
       
       self.logger.info("Visited %s", response.url)
       print(response.url)
       print(page_data)

process = CrawlerProcess()
process.crawl(JobSpider)
process.start() 
