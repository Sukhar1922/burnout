from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.db import connection
from django.core.cache import cache
from django.db import transaction

from .models import Questions
from .models import People
from .models import Phase_VOLTAGE
from .models import Phase_EXHAUSTION
from .models import Phase_RESISTANCE
from .models import Test_Burnout

import json
from .BurnoutLib.BurnoutLib import HandlerQuestions
import time

# Create your views here.

def test(request):
    return JsonResponse({'success': 'True'}, status=200)


def GETquestions(request):
    if request.method == 'GET':
        data = cache.get('questions_cache')
        # print(f'Кэш {data}')
        if data is None:
            data = list(Questions.objects.values('id', 'Name_Question'))
            cache.set('questions_cache', data, timeout=None)
            # print('Создан кэш для таблицы вопросов')
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


def POSTregistration(request):
    if request.method == 'POST':
        data = {}
        for key, value in request.POST.items():
            data[key] = value
        # print(data)
        return JsonResponse(data, safe=False)

    return HttpResponseNotAllowed(['POST'])


def __addResultsToDB(people, testResults):
    with transaction.atomic():
        voltage = testResults[:4]
        resistance = testResults[4:8]
        exhaustion = testResults[8:]

        phaseVoltage = Phase_VOLTAGE.objects.create(
            People_ID=people,
            Symptom1=voltage[0],
            Symptom2=voltage[1],
            Symptom3=voltage[2],
            Symptom4=voltage[3],
            SymptomSum=sum(voltage)
        )
        phaseResistance = Phase_RESISTANCE.objects.create(
            People_ID=people,
            Symptom1=resistance[0],
            Symptom2=resistance[1],
            Symptom3=resistance[2],
            Symptom4=resistance[3],
            SymptomSum=sum(resistance)
        )
        phaseExhaustion = Phase_EXHAUSTION.objects.create(
            People_ID=people,
            Symptom1=exhaustion[0],
            Symptom2=exhaustion[1],
            Symptom3=exhaustion[2],
            Symptom4=exhaustion[3],
            SymptomSum=sum(exhaustion)
        )
        testBurnout = Test_Burnout.objects.create(
            People_ID=people,
            VOLTAGE=phaseVoltage,
            RESISTANCE=phaseResistance,
            EXHAUSTION=phaseExhaustion,
            Summary_Value=sum(testResults)
        )
        return (phaseVoltage, phaseResistance, phaseExhaustion, testBurnout)


def POSTanswers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        answers = data['Answers']
        TG_ID = data['TG_ID']
        people = People.objects.filter(TG_ID=TG_ID) # Можно будет бахнуть кэш
        result = {}
        # print(people[0])

        if len(people) == 1:
            t1 = time.time()
            hq = HandlerQuestions()
            testResults = hq.handle_answers(answers)
            __addResultsToDB(people[0], testResults)
            resultTime = time.time() - t1

            result['runTime'] = f'{resultTime:.5f} sec'
            result['testResults'] = testResults
        elif len(people) == 0:
            t1 = time.time()
            hq = HandlerQuestions()
            testResults = hq.handle_answers(answers)
            resultTime = time.time() - t1

            result['runTime'] = f'{resultTime:.5f} sec'
            result['testResults'] = testResults
        else:
            result['status'] = f'DB has more then one {TG_ID}'
        return JsonResponse(result, safe=False)

    return HttpResponseNotAllowed(['POST'])