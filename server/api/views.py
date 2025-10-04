from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.db import connection
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from .models import Questions, Everyweek_Tasks, Answers_Everyweek_Tasks, Options, Answers_Everyday
from .models import People
from .models import Test_Burnout

import json
from .BurnoutLib.BurnoutLib import HandlerQuestions, getFakeStatistics
import time
from datetime import datetime, timedelta, date

# Create your views here.

def test(request):
    return JsonResponse({'success': 'True'}, status=200)


def GETquestions(request):
    if request.method == 'GET':
        TG_ID = request.GET.get('TG_ID')
        if TG_ID is None:
            return JsonResponse({'status': 'Needs TG_ID field'}, status=401, safe=False)
        people = People.objects.filter(TG_ID=TG_ID).first()
        if people is None:
            return JsonResponse({'status': 'There is no user with this TG_ID'}, status=401, safe=False)

        month_ago = timezone.localtime() - timedelta(days=31)
        active_test_exists = Test_Burnout.objects.filter(
                Date_Record__gte=month_ago,
                People_ID=people,
            ).exists()

        if active_test_exists:
            return JsonResponse({'status': 'There is an active test'}, status=403, safe=False)

        active_burnout_test_exists = Test_Burnout.objects.filter()
        data = cache.get('questions_cache')
        # print(f'Кэш {data}')
        if data is None:
            data = list(Questions.objects.values('id', 'Name_Question'))
            cache.set('questions_cache', data, timeout=None)
            # print('Создан кэш для таблицы вопросов')
        return JsonResponse(data, safe=False)

    return HttpResponseNotAllowed(['GET'])


def POSTregistration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        TG_ID = data['TG_ID']
        params_exist = \
            (People.objects.filter(TG_ID=TG_ID).exists() and People.objects.filter(Nickname=data['Nickname']).exists())

        if params_exist:
            return JsonResponse({'status': 'TG_ID or Nickname exists'}, status=403)

        newPeople = People.objects.create(
            Nickname=data['Nickname'],
            Email=data['Email'],
            Work_Experience=data['Work_Experience'],
            Birthday=data['Birthday'],
            TG_ID=TG_ID
        )
        return JsonResponse({'status': 'success'}, status=201, safe=False)

    return HttpResponseNotAllowed(['POST'])


def GETcheckNickname(request):
    if request.method == 'GET':
        Nickname = request.GET.get('Nickname')
        is_exists = People.objects.filter(Nickname=Nickname).exists()
        if is_exists:
            return JsonResponse({'status': 'exists'})
        return JsonResponse({'status': 'does not exist'})

    return HttpResponseNotAllowed(['GET'])


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
        if 'TG_ID' in data:
            TG_ID = data['TG_ID']
        else:
            TG_ID = ''
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
            # print(testResults)
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
            result = len(people) != 0

        return JsonResponse({'isTherePeople': result}, safe=False)
    return HttpResponseNotAllowed(['GET'])


def EvereweekTasks(request):
    if request.method == 'GET':
        TG_ID = request.GET.get('TG_ID')
        people = People.objects.filter(TG_ID=TG_ID).first()
        if people is not None:
            last_test_burnout = Test_Burnout.objects.filter(People_ID=people).order_by('-Date_Record').values().first()
            if last_test_burnout is None:
                return JsonResponse({'status': 'There are no tests'}, status=404)
            if last_test_burnout['Date_Record'].date() + timedelta(days=31) < date.today():
                return JsonResponse({'status': 'The test was a long time ago'}, status=410)
            sums = {
                'Напряжение': last_test_burnout['Voltage_symptomSum'],
                'Резистенция': last_test_burnout['resistance_symptomSum'],
                'Истощение': last_test_burnout['exhaustion_symptomSum'],
            }
            max_phase = max(sums, key=sums.get)
            everyweek_task_types = Everyweek_Tasks.objects.filter(Phase=max_phase).values()
            result = {}
            tasks = []
            for everyweek_task_type in everyweek_task_types:
                tasks.append(everyweek_task_type)
            result['tasks'] = tasks
            task_history = Answers_Everyweek_Tasks.objects.filter(TestID=last_test_burnout['id']).order_by('-Date_Record')
            took_tasks = []
            for test in task_history:
                took_tasks.append(test.TaskID.id)
            result['took_tasks'] = took_tasks
            last_task = task_history.values('TaskID_id', 'Date_Record', 'Stars', 'Comments').first()
            result['last_task'] = last_task
            return JsonResponse(result, safe=False)
        return JsonResponse({'status': 'There is no such user or empty TG_ID'}, status=404)

    elif request.method == 'POST':
        data = json.loads(request.body)
        if not ('TG_ID' in data and 'TaskID' in data):
            return JsonResponse({'status': 'TG_ID and TaskID are required'}, status=400)
        TG_ID = data['TG_ID']
        TaskID = data['TaskID']
        people = People.objects.filter(TG_ID=TG_ID).first()
        if people is None:
            return JsonResponse({'status': f'There is no such people with such TG_ID: {TG_ID}'}, status=404)
        last_test_burnout = Test_Burnout.objects.filter(People_ID=people).order_by('-Date_Record').first()
        if last_test_burnout is None:
            return JsonResponse({'status': f'There are no tests yet'}, status=404)

        answers_everyweek_tasks_with_no_stars = Answers_Everyweek_Tasks.objects.filter(
            TestID=last_test_burnout,
            Stars=None,
        ).values()
        if len(answers_everyweek_tasks_with_no_stars) > 0:
            return JsonResponse({'status': f'There is a test with 0 stars'}, status=403)

        if last_test_burnout.Date_Record.date() + timedelta(days=31) < date.today():
            return JsonResponse({'status': 'The test was a long time ago'}, status=410)
        task = Everyweek_Tasks.objects.filter(id=TaskID).first()
        if task is None:
            return JsonResponse({'status': f'There is no task type with id={TaskID}'}, status=404)

        answer_everyweek_task = Answers_Everyweek_Tasks.objects.create(
            TestID=last_test_burnout,
            TaskID=task,
        )
        return JsonResponse({'status': f'Task created with id={answer_everyweek_task.id}'}, status=201)

    elif request.method == 'PATCH':
        data = json.loads(request.body)
        if not ('TG_ID' in data and 'Stars' in data and 'Comments' in data):
            return JsonResponse({'status': 'TG_ID, Stars and Comments are required'}, status=400)
        TG_ID = data['TG_ID']
        Stars = int(data['Stars'])
        Comments = data['Comments']
        people = People.objects.filter(TG_ID=TG_ID).first()
        if people is None:
            return JsonResponse({'status': f'There is no such people with such TG_ID: {TG_ID}'}, status=404)
        if not (1 <= Stars <= 5):
            return JsonResponse({'status': f'The number of Stars should be from 1 to 5'}, status=400)
        last_test_burnout = Test_Burnout.objects.filter(People_ID=people).order_by('-Date_Record').first()
        if last_test_burnout is None:
            return JsonResponse({'status': f'There are no tests yet'}, status=404)

        if not (last_test_burnout.Date_Record.date() + timedelta(days=7) < date.today()):
            return JsonResponse({'status': f'Still waiting a week...'}, status=403)

        answer_everyweek_task = Answers_Everyweek_Tasks.objects.filter(TestID=last_test_burnout)\
            .order_by('-Date_Record').first()
        if answer_everyweek_task.Stars is not None:
            return JsonResponse({'status': f'Stars were here before'}, status=403)
        answer_everyweek_task.Stars = Stars
        answer_everyweek_task.Comments = Comments
        answer_everyweek_task.save()
        return JsonResponse({'status': f'Task updated with {Stars} stars'}, status=200)

    return HttpResponseNotAllowed(['GET', 'POST', 'PATCH'])


# def TestTG(request):
#     send_telegram_message('2044308378', 'Для улучшения эмоционального состояния рекомендуется удалить '
#                                         'следующее вредоносное ПО: Overwatch 2, Deadlock')
#     return JsonResponse({}, status=200)


def OptionsAPI(request):
    if request.method == 'GET':
        TG_ID = request.GET.get('TG_ID')
        people = People.objects.filter(TG_ID=TG_ID).first()
        if people is None:
            return JsonResponse({'status': f'There is no such people with such TG_ID: {TG_ID}'}, status=404)

        options = Options.objects.filter(People_ID=people).values('Notification_Day',
                                                                 'Notification_Week',).first()
        options['Email'] = people.Email
        return JsonResponse(options, status=200, safe=False)

    elif request.method == 'PATCH':
        data = json.loads(request.body)
        if 'TG_ID' not in data:
            return JsonResponse({'status': 'TG_ID is required'}, status=400)

        TG_ID = data['TG_ID']
        people = People.objects.filter(TG_ID=TG_ID).first()
        if people is None:
            return JsonResponse({'status': f'There is no such people with such TG_ID: {TG_ID}'}, status=404)

        options = Options.objects.filter(People_ID=people).first()
        if options is None:
            return JsonResponse({'status': 'Options not found for this person'}, status=404)

        allowed_fields = {
            'Notification_Day',
            'Notification_Day_Time',
            'Notification_Week',
            'Notification_Week_Time',
            'Email',
        }

        update_options = {}
        update_people = {}

        for key, value in data.items():
            if key == 'TG_ID':
                continue
            if key not in allowed_fields:
                return JsonResponse({'status': f'Field {key} is not allowed'}, status=400)

            if key == 'Email':
                update_people['Email'] = value
            else:
                update_options[key] = value

        if update_people:
            for k, v in update_people.items():
                setattr(people, k, v)
            people.save(update_fields=list(update_people.keys()))

        if update_options:
            for k, v in update_options.items():
                setattr(options, k, v)
            options.save(update_fields=list(update_options.keys()))

        return JsonResponse({'status': 'Updated'}, status=200)
    return HttpResponseNotAllowed(['GET', 'PATCH'])


def sendEveryDayAnswers(request):
    if request.method == "GET":
        TG_ID = request.GET.get('TG_ID')
        people = People.objects.filter(TG_ID=TG_ID).first()
        if people is None:
            return JsonResponse({'status': f'There is no such people with such TG_ID: {TG_ID}'}, status=404)

        today = timezone.now().date()
        # today = date.today()
        was_today_answer = Answers_Everyday.objects.filter(Created_at__date=today, People_ID=people).exists()
        if was_today_answer:
            return JsonResponse({'Can I send the answer': 'False'}, status=200)
        return JsonResponse({'Can I send the answer': 'True'}, status=200)

    elif request.method == "POST":
        data = json.loads(request.body)
        TG_ID = data['TG_ID']
        answers = data['Answers']
        people = People.objects.filter(TG_ID=TG_ID).first()
        if people is None:
            return JsonResponse({'status': f'There is no such people with such TG_ID: {TG_ID}'}, status=404)

        today = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
        was_today_answer = Answers_Everyday.objects.filter(Created_at__gt=today, People_ID=people).exists()
        if was_today_answer:
            return JsonResponse({'status': 'There was today\'s answer'}, status=403)

        if not ('Emotional_Condition' in answers
                and 'Physical_Condition' in answers
                and 'Burnout' in answers):
            return JsonResponse({'status': 'Emotional_Condition, Physical_Condition, Burnout are required'}, status=400)

        try:
            # сделать проверку на введённые данные в [1, 3]
            conditions = ['Emotional_Condition', 'Physical_Condition', 'Burnout']
            for condition in conditions:
                if not (1 <= answers[condition] <= 3):
                    return JsonResponse({'status': 'conditions must be in [1, 3]'}, status=400)

            Answers_Everyday.objects.create(
                People_ID=people,
                Emotional_Condition=answers['Emotional_Condition'],
                Physical_Condition=answers['Physical_Condition'],
                Burnout=answers['Burnout'],
            )

            return JsonResponse({'status': 'added'}, status=201)
        except Exception as e:
            return JsonResponse({'status': f'[DjangoError]: {e}'}, status=500)

    return HttpResponseNotAllowed(['GET', 'POST'])


def GETeverydayStatistics(request):
    if request.method == 'GET':
        TG_ID = request.GET.get('TG_ID')
        if TG_ID is None:
            return JsonResponse({'status': 'Needs TG_ID field'}, status=401, safe=False)
        person = People.objects.filter(TG_ID=TG_ID).first()
        results = []

        if person is None:
            return JsonResponse({'status': f'There is no person with this {TG_ID} TG_ID'}, status=404, safe=False)

        answers_everyday = Answers_Everyday.objects.filter(People_ID=person)

        for answer_everyday in answers_everyday:
            conditions = [
                answer_everyday.Emotional_Condition,
                answer_everyday.Physical_Condition,
                answer_everyday.Burnout,
            ]

            node = [
                {'time': int(answer_everyday.Created_at.timestamp())},
                conditions
            ]

            results.append(node)
        return JsonResponse(results, status=200, safe=False)

    return HttpResponseNotAllowed(['GET'])

def GETeveryweekStatistics(request):
    if request.method == 'GET':
        TG_ID = request.GET.get('TG_ID')
        if TG_ID is None:
            return JsonResponse({'status': 'Needs TG_ID field'}, status=401, safe=False)
        person = People.objects.filter(TG_ID=TG_ID).first()
        results = []

        if person is None:
            return JsonResponse({'status': f'There is no person with this {TG_ID} TG_ID'}, status=404, safe=False)

        tests_burnout = Test_Burnout.objects.filter(People_ID=person)
        for test_burnout in tests_burnout:
            answers_everyweek = Answers_Everyweek_Tasks.objects.filter(TestID=test_burnout) \
                    .select_related("TaskID")

            for answer_everyweek in answers_everyweek:
                answers = [
                    answer_everyweek.Stars,
                    answer_everyweek.Comments,
                    answer_everyweek.TaskID.Name,
                    answer_everyweek.TaskID.Phase,
                ]

                node = [
                    {'time': int(answer_everyweek.Date_Record.timestamp())},
                    answers
                ]

                results.append(node)
        return JsonResponse(results, status=200, safe=False)
    return HttpResponseNotAllowed(['GET'])
