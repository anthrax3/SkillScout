#-*- coding: utf-8 -*-
"""
Web scraper built using the Scrapy framework
@author: stephen schneider
"""
import os
import scrapy
import sys
from datetime import datetime, timedelta
# enter working directory: os.chdir('/home/stephen/Code/Python/venv/SkillScout/backend')
# Add directory to path: sys.path.append('/home/stephen/Code/Python/venv/SkillScout/backend')
#import module to connect to postgresql
#import psycopg2
#conn = psycopg2.connect(dsn)

from scrapy.crawler import CrawlerProcess
    

class JobSpider(scrapy.Spider):
    from secret_settings import *
    name = 'jobspider'
    allowed_domains = ['www.indeed.com']
    
    #Ask for user input
    
    #user_city = raw_input("Enter city:\n")
    user_city = 'San Francisco'
    city_name = user_city.replace(" ", "+")
    #state_name = raw_input("Enter state abbreviation:\n")
    state_name = 'CA'
    start_urls = ['https://www.indeed.com/jobs?q=&l=' + city_name + '%2C+' + state_name + '&sort=date']
    #counts and extracts document links from followed link :
    main_table = '/html/body/table[2]/tr/td/table/tr/td[2]'
    abs_link = 'https://www.indeed.com'
    #control page range here!
    #request how many pages to scrape
    pg_limit = 2
    verify_page_scrape = []
    check_repeats = set()
    pg_counter = 0     
       
    def parse(self, response): 
        scrape_date = datetime.today().strftime('%m-%d-%Y')
        
        #Check if first link is non-sponsored..-_-
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
        
        self.pg_counter = self.pg_counter + 1    
        print 'response url of page %s is : %s' % (self.pg_counter, response.url)
        self.verify_page_scrape.extend([self.pg_counter, response.url[-3:]])
     
     # if response.url[-2:] != 'te' and int(response.url[-2:]< 100) and response.url[-2:] != str((self.pg_counter-1)*10):
          #  print 'error in page called'
        
        #change link of next page, depending on current page
        if self.pg_counter > self.pg_limit:
            print('Page limit reached, Closing Scraper')
            print(self.verify_page_scrape)
            sys.exit()
        elif self.pg_counter == 1:
            next_page_loc = 5
        elif self.pg_counter == 2:
            next_page_loc = 7
        elif self.pg_counter == 3:
            next_page_loc = 8
        elif self.pg_counter == 4:
            next_page_loc = 9
        elif self.pg_counter <= self.pg_limit:
            next_page_loc = 10
        
        
        for link_num in range(0,10):
            
            #location of doc info: url, title, date 
            info_location = self.main_table + '/div[' + str(start_int + link_num)
            url_location = info_location +']/h2/a/@href'
            title_location = info_location + ']/h2/a/@title' 
            job_date_location = info_location + ']/table/tr/td//div[contains\
            (@class, "result-link-bar-container")]/div[1]//span[contains(@class, "date")]/text()'

            #actual doc info: url, title, date
            job_url = str(self.abs_link + response.xpath(str(url_location)).extract_first())
            job_title = str(response.xpath(str(title_location)).extract_first())
            job_date = str(response.xpath(str(job_date_location)).extract_first())
            if job_date == 'Just posted' or job_date == 'Today':
                job_date = scrape_date
            elif job_date[-3:] == 'ago':
                days_ago = int(job_date.split()[0])
                d = datetime.today() - timedelta(days = days_ago)
                job_date = d.strftime('%m-%d-%Y')
                
            #combined data per link
            info_per_link = [job_title, job_date]
            print 'Getting request from link %s' % (link_num + 1)
            request = scrapy.Request(job_url, callback = self.get_html)
            request.meta['info_per_link'] = info_per_link
            next_page = self.main_table + '//div[contains(@class, "pagination")]/a[' + str(next_page_loc) + ']/@href'
            next_page_link = self.abs_link + str(response.xpath(next_page).extract_first())
            request.meta['next_page_link'] = next_page_link 
            
            yield request

       
    
    def get_html(self, response):
        output_loc = '/home/stephen/Code/Python/venv/SkillScout/backend/html_out'
        # retrieve info per link to group with downloaded htmls
        info_per_link = response.meta['info_per_link']
        job_url = response.url
        job_title = info_per_link[0]        
        job_date = info_per_link[1]
        job_city = self.user_city
        #add date + url to set...
        verify_filename = os.path.join(output_loc, job_date + '.txt')
        count_file = os.path.join(output_loc, 'Count.txt')
        # if file can be opened, read it, and append to it if job_url is not in it.
        print 'checking for repeats...'        
        try: 
            with open(verify_filename) as f:
                check_repeats = f.readlines()
            check_repeats = [x.strip() for x in check_repeats]
            with open(verify_filename, 'a') as f:
                if job_url not in check_repeats:
                    print 'url is unique'
                    f.write(job_url + '\n')
                    print 'Saving metadata to SQL'
                    ### open sql to view last doc downloaded for count???
                    with open(count_file, 'r') as f:
                        doc_count = f.readline()
                    total_doc_count = doc_count.strip()
                    
                    filename = os.path.join(output_loc, total_doc_count + '.html')
                    #save file:
                    with open(filename, 'wb') as f:
                        f.write(response.body)
                    os.chmod(filename, 0555) 
                    #count documents downloaded
                    print 'Downloading document %s\ntitle: %s\ndate: %s\nurl:  %s' % (total_doc_count, job_title, job_date, response.url)
                    total_doc_count = str(int(total_doc_count) + 1)
                    #increment total doc_count
                    with open(count_file, 'wb') as f:
                        f.write(total_doc_count)
                else:
                    print 'url is not uniqe \nSkipping download, document already downloaded'  
        # if file cannot be opened, write it and append url to last line. 
       # this means no other docs have been downloaded for this date yet, no need to check for redundancy...
        except IOError:
            with open(verify_filename, 'wb') as f:
                f.write(job_url + '\n')
                print 'Saving metadata to SQL'
                with open(count_file, 'r') as f:
                    doc_count = f.readline()
                total_doc_count = doc_count.strip()
                
                filename = os.path.join(output_loc, total_doc_count + '.html')
                #save file:
                with open(filename, 'wb') as f:
                    f.write(response.body)
                os.chmod(filename, 0555) 
                #count documents downloaded
                print 'Downloading document %s\ntitle: %s\ndate: %s\nurl:  %s' % (total_doc_count, job_title, job_date, response.url)

                total_doc_count = str(int(total_doc_count) + 1)
                with open(count_file, 'wb') as f:
                    f.write(total_doc_count)
                                   
            
        self.logger.info('visited %s', response.url)

        #filename is shortened to 150 characters without .html      
        #short_name = response.url.split('/')[-1][0:150]
        #only add .html if missing...
        #add doc_count to end of filename for uniqueness?
#        if short_name[-5:] == '.html':
#            filename = os.path.join(output_loc, short_name + str(self.doc_counter))
#        else:
#            filename = os.path.join(output_loc, short_name + str(self.doc_counter) + '.html')
        
        next_page_link = response.meta['next_page_link']
        print 'Requesting next page link: %s' % (next_page_link)
        request = scrapy.Request(next_page_link, callback = self.parse)
        return request              
        

process = CrawlerProcess()
process.crawl(JobSpider)
process.start() 
