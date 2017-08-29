# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 15:09:21 2017
Functions in use  for jobscraper.py
@author: stephen
"""

def scrape_link(main_table, scrape_date, start_int, response):
   abs_link = 'https://www.indeed.com'
   page_data = []
   for link_num in range(0,10):
      info_location = main_table + '/div[' + str(start_int + link_num)
      url_location = info_location +']/h2/a/@href'
      title_location = info_location + ']/h2/a/@title' 
      job_url = str(abs_link + response.xpath(str(url_location)).extract_first())
      job_title = str(response.xpath(str(title_location)).extract_first())
      job_date = scrape_date
      info_per_link = [job_url,job_title,job_date]
      page_data.append(info_per_link)
   return page_data
