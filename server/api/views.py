from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.db import connection
from django.core.cache import cache
from django.db import transaction

from .models import Questions
from .models import People
from .models import Test_Burnout

import json
from .BurnoutLib.BurnoutLib import HandlerQuestions, getFakeStatistics
import time
from datetime import datetime

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
        result = {'status': 'success'}
        data = json.loads(request.body)
        TG_ID = data['TG_ID']
        people = People.objects.filter(TG_ID=TG_ID)
        if len(people) == 0:
            newPeople = People.objects.create(
                Name=data['Name'],
                Surname=data['Surname'],
                Patronymic=data['Patronymic'],
                Email=data['Email'],
                Birthday=data['Birthday'],
                TG_ID=TG_ID
            )
        else:
            result['status'] = 'failure'
        return JsonResponse(result, safe=False)

    return HttpResponseNotAllowed(['POST'])


def __addResultsToDB(people, hq):
    # with transaction.atomic():
    voltage = hq.PhaseVoltage
    resistance = hq.PhaseResistance
    exhaustion = hq.PhaseExhaustion

    # print(f'voltage.points() {voltage.points}')
    testBurnout = Test_Burnout.objects.create(
        People_ID=people,
        Voltage_symptom1=voltage.Symptom(1).points,
        Voltage_symptom2=voltage.Symptom(2).points,
        Voltage_symptom3=voltage.Symptom(3).points,
        Voltage_symptom4=voltage.Symptom(4).points,
        Voltage_symptomSum=voltage.points,
        resistance_symptom1=resistance.Symptom(1).points,
        resistance_symptom2=resistance.Symptom(2).points,
        resistance_symptom3=resistance.Symptom(3).points,
        resistance_symptom4=resistance.Symptom(4).points,
        resistance_symptomSum=resistance.points,
        exhaustion_symptom1=exhaustion.Symptom(1).points,
        exhaustion_symptom2=exhaustion.Symptom(2).points,
        exhaustion_symptom3=exhaustion.Symptom(3).points,
        exhaustion_symptom4=exhaustion.Symptom(4).points,
        exhaustion_symptomSum=exhaustion.points,
        Summary_Value=hq.points,
    )
    return (testBurnout)


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
            __addResultsToDB(people[0], hq)
            resultTime = time.time() - t1

            result['runTime'] = f'{resultTime:.5f} sec'
            result['testResults'] = testResults
            result['status'] = 'inserted'
        elif len(people) == 0:
            t1 = time.time()
            hq = HandlerQuestions()
            testResults = hq.handle_answers(answers)
            print(testResults)
            resultTime = time.time() - t1

            result['runTime'] = f'{resultTime:.5f} sec'
            result['testResults'] = testResults
            result['status'] = 'DB has not changed'
        else:
            result['status'] = f'DB has more then one {TG_ID}'
        return JsonResponse(result, safe=False)
    return HttpResponseNotAllowed(['POST'])


def GETstatistics(request):
    if request.method == 'GET':
        t1 = time.time()
        TG_ID = request.GET.get('TG_ID')
        people = People.objects.filter(TG_ID=TG_ID)
        result = []

        if len(people) != 1:
            return JsonResponse({'status': 'Some problems with TG_ID'}, safe=False)

        people = people[0]
        testBurnouts = Test_Burnout.objects.filter(People_ID=people)

        for testBurnout in testBurnouts:
            symptoms = []
            # voltage = testBurnout.VOLTAGE
            # resistance = testBurnout.RESISTANCE
            # exhaustion = testBurnout.EXHAUSTION

            symptoms.append(testBurnout.Voltage_symptom1)
            symptoms.append(testBurnout.Voltage_symptom2)
            symptoms.append(testBurnout.Voltage_symptom3)
            symptoms.append(testBurnout.Voltage_symptom4)

            symptoms.append(testBurnout.resistance_symptom1)
            symptoms.append(testBurnout.resistance_symptom2)
            symptoms.append(testBurnout.resistance_symptom3)
            symptoms.append(testBurnout.resistance_symptom4)

            symptoms.append(testBurnout.exhaustion_symptom1)
            symptoms.append(testBurnout.exhaustion_symptom2)
            symptoms.append(testBurnout.exhaustion_symptom3)
            symptoms.append(testBurnout.exhaustion_symptom4)

            node = [
                {'time': int(testBurnout.Date_Record.timestamp())},
                getFakeStatistics(symptoms)
            ]

            result.append(node)
        runtime = time.time() - t1
        print(f'runtime {runtime:.5f} sec')
        return JsonResponse(result, safe=False)

    return HttpResponseNotAllowed(['GET'])


def GETcheckPeople(request):
    if request.method == 'GET':
        result = False
        TG_ID = request.GET.get('TG_ID')
        if TG_ID is None:
            result = 'Needs TG_ID field'
        else:
            people = People.objects.filter(TG_ID=TG_ID) # Можно лупануть кэш
            if len(people) != 0:
                result = True

        return JsonResponse({'isTherePeople': result}, safe=False)
    return HttpResponseNotAllowed(['GET'])