from django.db import models
from django.utils import timezone
import json

# 修改model之后要
# python manage.py makemigrations
# python manage.py migrate

# Create your models here.
class Article(models.Model):
    source = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=True)
    url = models.URLField(null=True)
    date = models.CharField(max_length=100, null=True)
    keyword = models.CharField(max_length=100, null=True)
    text = models.TextField(null=True)
    
    # @property
    # def to_dict(self):
    #     data = {
    #         'source': self.source,
    #         'title': self.title,
    #         'url': self.url,
    #         'date': self.date,
    #         'text': self.text
    #     }
