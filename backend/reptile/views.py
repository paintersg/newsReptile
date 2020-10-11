from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from scrapyd_api import ScrapydAPI
from reptile.models import Article
import time
import json

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


# def is_valid_url(url):
#     validate = URLValidator()
#     try:
#         validate(url)  # check if url format is valid
#     except ValidationError:
#         return False

#     return True
def listToDict(l):
    i = 0
    d = {}
    for e in l:
        d[str(i)] = e
        i = i + 1
    return d

@csrf_exempt
@require_http_methods(['POST', 'GET'])
def gzdaily(request):
    if request.method == 'POST':
        Article.objects.filter(source='广州日报').delete()
        keywordsList = json.loads(request.body)['keywords']
        keywordsDict = listToDict(keywordsList)
        print(keywordsDict)
        taskId = scrapyd.schedule('default', 'gzdaily', **keywordsDict)
        return JsonResponse({ 'msg': 'OK', 'task': { 'id': taskId, 'source': '广州日报' } })


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def huxiu(request):
    if request.method == 'POST':
        Article.objects.filter(source='虎嗅网').delete()
        keywordsList = json.loads(request.body)['keywords']
        # keywordsList = ['记者', '时间']
        keywordsDict = listToDict(keywordsList)
        taskId = scrapyd.schedule('default', 'huxiu', **keywordsDict)
        return JsonResponse({'msg': 'OK', 'task': {'id': taskId, 'source': '虎嗅网'}})


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def results(request):
    if request.method == 'GET':
        taskList = []
        for k, v in request.GET.items():
            taskList.append(json.loads(v))

        taskResults = []
        for task in taskList:
            if scrapyd.job_status('default', task['id']) == 'finished':
                tempResult = { 'id': task['id'], 'results': [] }
                atcs = Article.objects.filter(source=task['source'])
                for item in atcs:
                    tempResult['results'].append({
                        'id': item.id,
                        'title': item.title,
                        'url': item.url
                    })
                taskResults.append(tempResult)
        
        return JsonResponse({'msg': 'OK', 'data': taskResults}, safe=False)

