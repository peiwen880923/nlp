import requests
import scrapy
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
class DronesspiderSpider(scrapy.Spider):
    name = 'stackexchange'
    #start_urls=['https://stackexchange.com/?page=1','https://stackexchange.com/?page=2','https://stackexchange.com/?page=3','https://stackexchange.com/?page=4']
    start_urls=['https://stackexchange.com/?page=1']
    def parse(self,response):
        all=response.css('div.question.question-hot')
        for all1 in all:
            dict1={
                'title':all1.css('a.question-link::text').get().replace('             ','').replace('\n   ',"").replace('    ',''),
                'tag':all1.css('a.post-tag::text').getall(),
                'author':all1.css('span.owner a::text').get(),
                'link':all1.css('a.question-link::attr(href)').get(),  
            }
            link=all1.css('a.question-link::attr(href)').get()
            soup = requests.get(link)
            soup=BeautifulSoup(soup.text,'lxml')
            contents=soup.find_all('div','postcell post-layout--right')
            for content in contents:
                text=content.find('div','s-prose js-post-body')
                dict1['content']=text.text
            yield dict1