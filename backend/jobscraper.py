#-*- coding: utf-8 -*-
"""
Web scraper built using the Scrapy framework
@author: stephen schneider
"""
import os
import scrapy
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
    main_table = '/html/body/table[2]/tr/td/table/tr/td[2]'
    abs_link = 'https://www.indeed.com'
    #control page range here!
    #request how many files to download in multiples of 10:
    doc_limit = 40    
    
    doc_counter = 0
    
     
       
    def parse(self, response): 
        scrape_date = datetime.date.today().strftime('%m-%d-%Y')
        
        #Check if first link is non-sponsored..
        first_link = response.xpath(self.main_table + '/div[4]').extract_first()
        if first_link[14:25] == u'row  result':
            print('The first link starts at the 4th div')
            start_int = 4 
        else:
            first_link = response.xpath(self.main_table + '/div[5]').extract_first()
            if first_link[14:25] == u'row  result':
                print('The first link starts at the 5th div')
                start_int = 5
            else:
                first_link = response.xpath(self.main_table + '/div[6]').extract_first()
                print('The first link starts at the 6th div')
                start_int = 6
        
        
        for link_num in range(0,10):
            info_location = self.main_table + '/div[' + str(start_int + link_num)
            url_location = info_location +']/h2/a/@href'
            title_location = info_location + ']/h2/a/@title' 
            job_url = str(self.abs_link + response.xpath(str(url_location)).extract_first())
            job_title = str(response.xpath(str(title_location)).extract_first())
            job_date = scrape_date
            info_per_link = [job_url,job_title,job_date]
            print 'Getting request from link %s' % (link_num)
            request = scrapy.Request(job_url, callback = self.get_html)
            next_page = self.main_table + '//div[contains(@class, "pagination")]/a[5]/@href'
            first_follow = self.abs_link + str(response.xpath(next_page).extract_first())
            request.meta['first_follow'] = first_follow
            #print 'Getting first meta request'
            next_page_2 = self.main_table + '//div[contains(@class, "pagination")]/a[7]/@href'
            second_follow = self.abs_link + str(response.xpath(next_page_2).extract_first())
            request.meta['second_follow'] = second_follow
            #print 'Getting second meta request'
            request.meta['info_per_link'] = info_per_link
            yield request
           
    
    def get_html(self, response):
        output_loc = '/home/stephen/Code/Python/venv/SkillScout/backend/html_out' 
        #filename is shortened to 150 characters without .html      
        short_name = response.url.split('/')[-1][0:150]
        filename = os.path.join(output_loc, short_name + self.doc_counter + '.html')
        #download file:
        with open(filename, 'wb') as f:
            f.write(response.body)
        os.chmod(filename, 0555)           
        self.logger.info('visited %s', response.url)
        print 'Downloading html from %s' % (response.url)
        #count documents downloaded
        self.doc_counter = self.doc_counter + 1
        print 'on document %s' % (self.doc_counter)
        if self.doc_counter == 10:
            print 'following first meta request'
            first_follow = response.meta['first_follow']
            print first_follow
            request = scrapy.Request(first_follow, callback = self.parse)
            yield request
        elif self.doc_counter > 10 and self.doc_counter < (self.doc_limit) and self.doc_counter%10 == 0:
            print 'following second meta request' 
            print 'on document %s' % (self.doc_counter)
            second_follow = response.meta['second_follow']
            print second_follow
            request = scrapy.Request(second_follow, callback = self.parse)
            yield request
            
                    

process = CrawlerProcess()
process.crawl(JobSpider)
process.start() 
