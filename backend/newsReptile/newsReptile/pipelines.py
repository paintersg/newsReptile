# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from reptile.models import Article
from scrapy.exceptions import DropItem
import time

class NewsreptilePipeline(object):
    def __init__(self):
        self.urlSet = set()

    def process_item(self, item, spider):
        # 单次查询时，查询结果的内部去重[article1, article1, article2] -> [article1, article2]
        if item['url'] in self.urlSet:
            raise DropItem('Duplicate article')

        self.urlSet.add(item['url'])

        # base_dir = os.getcwd()
        # # filename = os.path.join(base_dir, 'data', item['title'] + '.txt')
        # filename = os.path.join(base_dir, 'data', str(time.time()) + '.txt')
        # # filename = base_dir + '\data\\' + item['title'] + '.txt'
        # with open(filename, 'w', encoding='utf-8') as f:
        #     f.write(item['source'] + '\n')
        #     f.write(item['title'] + '\n')
        #     f.write(item['url'] + '\n')
        #     f.write(item['date'] + '\n')
        #     f.write(item['keyword'] + '\n')
        #     f.write(item['text'] + '\n\n')

        article = Article()
        article.source = item['source']
        article.title = item['title']
        article.url = item['url']
        article.date = item['date']
        article.keyword = item['keyword']
        article.text = item['text']

        

        article.save()

        return item
