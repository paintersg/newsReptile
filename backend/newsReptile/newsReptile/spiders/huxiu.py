# -*- coding: utf-8 -*-
import scrapy
from newsReptile.items import Article
import datetime
from scrapy.selector import Selector

class HuxiuSpider(scrapy.Spider):
    name = 'huxiu'

    def __init__(self, *args, **kwargs):
        super(HuxiuSpider, self).__init__(*args, **kwargs)

        self.allowed_domains = ['huxiu.com']

        self.keywords = []
        for k, v in kwargs.items():
            if k.isdigit():
                self.keywords.append(v)

        # print('????????????????')
        # print(kwargs)
        # print('????????????????')

        baseUrl = 'https://www.huxiu.com/search.html?s='
        if len(self.keywords) > 0:
          baseUrl = baseUrl + self.keywords[0]
        for keyword in self.keywords[1:]:
            baseUrl = baseUrl + '%20' + keyword

        baseUrl = baseUrl + '&sort=dateline:desc'

        self.start_urls = [baseUrl,
                           baseUrl + '&per_page=2',
                           baseUrl + '&per_page=3']


    def parse(self, response):
        lists = response.xpath('//ul[@class="search-wrap-list-ul"]//li').extract()
        article = Article()
        article['source'] = '虎嗅网'

        timed = datetime.timedelta(3)
        today = datetime.datetime.now()

        for li in lists:
            print('**************************************')
            newsTime = Selector(text=li).xpath('//span[@class="time"]/text()').extract()[0]
            newsDatetime = datetime.datetime.strptime(newsTime, "%Y-%m-%d %H:%M")
            if today - newsDatetime <= timed:
                titleParts = Selector(text=li).xpath('//h2//text()').extract()
                title = ''
                for part in titleParts:
                    title = title + part

                url = Selector(text=li).xpath('//h2/a/@href').extract()[0]

                article['title'] = title
                article['url'] = 'https://www.huxiu.com' + url
                article['date'] = newsTime
                article['keyword'] = ''
                article['text'] = ''

                yield article
                

