#-*- coding: utf-8 -*-
"""
Web scraper built using the Scrapy framework
@author: stephen schneider
"""
import sys
sys.path.insert(0,"../utils")
from utils.skillscout_connection_utilities import PostgresqlDB
from utils.skillscout_connection_utilities import cleanHTML
import os
import scrapy
import sys
from datetime import datetime, timedelta
import psycopg2

# Connect to heroku postgresql
oPostgresql = PostgresqlDB()

from scrapy.crawler import CrawlerProcess


class JobSpider(scrapy.Spider):
    from secret_settings import *
    name = 'jobspider'
    allowed_domains = ['www.indeed.com']

    #Ask for user input

    #user_city = raw_input("Enter city: ")
    user_city = 'San Francisco'
    city_name = user_city.replace(" ", "+")
    #state_name = raw_input("Enter state abbreviation: ")
    state_name = 'CA'
    start_urls = ['https://www.indeed.com/jobs?q=&l=' + city_name + '%2C+' + state_name + '&sort=date']
    #counts and extracts document links from followed link :
    main_table = '/html/body/table[2]/tr/td/table/tr/td[2]'
    abs_link = 'https://www.indeed.com'
    #control page range here!
    #request how many pages to scrape
    #pg_limit = raw_input("Enter how many pages would you like to scrape: ")
    pg_limit = 10
    verify_page_scrape = []
    check_repeats = set()
    pg_counter = 0
    current_path = os.path.dirname(os.path.realpath('__file__'))
    print 'output directory must be in the SkillScout/backend/ directory and named "html_out"'
    output_dir = os.path.join(current_path,'../../backend/html_out')


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

        #change link of next page, depending on current page
        print "pg_counter:" + str(self.pg_counter)
        print "pg_limit:" + str(self.pg_limit)

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


        for link_num in range(10):
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
        # retrieve info per link to group with downloaded htmls
        info_per_link = response.meta['info_per_link']
        job_url = response.url
        job_title = info_per_link[0]
        job_date = info_per_link[1]
        job_city = self.user_city
        job_html = response.body
        job_text = cleanHTML(response.body)

        oPostgresql.execute("SELECT max(docid) FROM jobs;", "")
        max_id = oPostgresql.fetchone()
        if max_id[0] is None: # if table is brand new, there will be no max id yet
            total_doc_count = 0
        else:
            total_doc_count = max_id[0]
        #increment total_doc_count, then download w/ new doc_count as label
        doc_count = total_doc_count + 1
        #Fill a query
        print 'checking for repeats in primary key (url)...'
        try:
            oPostgresql.execute("INSERT INTO jobs (docid,title,date,city,urlid,html,raw) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (urlid) DO NOTHING",(doc_count,
            job_title,job_date,job_city,job_url,job_html,job_text))
            print 'no error, saving metadata to SQL and downloading document'
            oPostgresql.commit()


            #save file:
            # filename = os.path.join(self.output_dir, str(doc_count) + '.html')
            # with open(filename, 'wb') as f:
            #     f.write(response.body)
            #make read-only
            # os.chmod(filename, 0555)


            print 'Posted to Heroku Postgresql: document %s\ntitle: %s\ndate: %s\nurl:  %s' % (doc_count, job_title, job_date, response.url)

        except psycopg2.IntegrityError:
            print 'Integrity Error so table was left out... should also leave out downloading tho...'
            print 'url is not unique \nSkipping download, document already downloaded'
            oPostgresql.commit()


        self.logger.info('visited %s', response.url)


        next_page_link = response.meta['next_page_link']
        print 'Requesting next page link: %s' % (next_page_link)
        request = scrapy.Request(next_page_link, callback = self.parse)
        return request


process = CrawlerProcess()
process.crawl(JobSpider)
process.start()
