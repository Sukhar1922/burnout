from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.db import connection

from .models import Questions

from django.core.cache import cache
# Create your views here.

def test(request):
    return JsonResponse({'success': 'True'}, status=200)


def GETquestions(request):
    if request.method == 'GET':
        data = cache.get('questions_cache')
        print(f'Кэш {data}')
        if data is None:
            data = list(Questions.objects.values('id', 'Name_Question'))
            cache.set('questions_cache', data, timeout=None)
            print('Создан кэш для таблицы вопросов')
        return JsonResponse(data, safe=False)

    return HttpResponseNotAllowed(['GET'])


def fillQuestions(request):
    flag = False
    if not flag:
        return JsonResponse({'result': 'not allowed'}, safe=False)

    with open('api/SQL/Questions_fill.sql', encoding='utf-8') as f:
        content = f.read()
        result = __executeSQL(content)
        cache.delete('questions_cache')
        return JsonResponse(result, safe=False)


def __executeSQL(script):
    try:
        with connection.cursor() as cursor:
            scripts = script.split(';')
            for script in scripts:
                if script:
                    cursor.execute(f'{script};')
        return {'result': 'success'}
    except Exception:
        return {'result': str(Exception)}
