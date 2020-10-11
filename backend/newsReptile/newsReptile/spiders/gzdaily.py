# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector

from newsReptile.items import Article

class GzdailySpider(scrapy.Spider):
    name = 'gzdaily'
    allowed_domains = ['gzdaily.dayoo.com']

    baseUrl = 'http://gzdaily.dayoo.com/pc/html/'
    today = datetime.datetime.now()
    today = today - datetime.timedelta(days=1)

    dayurl = baseUrl + today.strftime('%Y-%m')+'/'
    dayurl = dayurl + today.strftime('%d')+'/'
    # 版面概览的网址
    indexurl = dayurl + 'index_' + today.strftime('%Y-%m-%d') + '.htm'

    start_urls = [indexurl]

    def __init__(self, *args, **kwargs):
        super(GzdailySpider, self).__init__(*args, **kwargs)

        # print()

        self.keywords = []
        for k, v in kwargs.items():
            if k.isdigit():
                self.keywords.append(v)
        
        # print('*********************************')
        # print(self.keywords)
        # print(len(self.keywords))
        # print('*********************************')


    def parse(self, response):
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        dayurl = response.url[:-20]
        links = response.xpath('//div[@class="paperList"]//a').extract()
        for link in links:
            # print(link)
            title = Selector(text=link).xpath('//text()').extract()[0]
            # print(title)
            url = dayurl + Selector(text=link).xpath('//@href').extract()[0]
            yield scrapy.Request(url=url,
                                 meta = { 'title': title, 'url': url, 'date': date },
                                 callback=self.parseArticle)
    
    def parseArticle(self, response):
        article = Article()
        article['source'] = '广州日报'
        article['title'] = response.meta['title']
        article['url'] = response.meta['url']
        article['date'] = response.meta['date']

        text = ''
        texts = response.xpath('//div[@id="ozoom"]//text()').extract()

        for t in texts:
            text = text + t
        
        text = text.replace('\u3000\u3000', '\n')
        text = text.replace(' ', '')
        text = text.replace('\r\n', '')
        text = text.replace('\t\n', '')
        article['text'] = text

        # 有关键词就输出
        for keyword in self.keywords:
            if text.find(keyword) != -1:
                article['keyword'] = keyword
                yield article
