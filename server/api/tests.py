import json
import os

from django.test import TestCase, Client
from .models import *
from .views import fillQuestions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_ADDRESS = '/django/api'

# Create your tests here.
class GETquestionsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/questions_368c231b7c9a3d506cef5a936c83d92f068179d849db19ac2608ba288c7c1c56'

        Questions.objects.create(
            Name_Question='Любите печеньки с молоком?',
            Points_Answer_Yes=100,
            Points_Answer_No=0,
        )
        Questions.objects.create(
            Name_Question='Любите маму с папой?',
            Points_Answer_Yes=50,
            Points_Answer_No=0,
        )

    def test_method_not_allowed(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_get_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['Name_Question'], 'Любите печеньки с молоком?')
        self.assertEqual(len(response.json()[1]), 2)

class POSTregistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/registration_8d6238094a7742ac22fedb3a180bc590d35f5ea70b8a262cc0bd976349b6181d'

    def test_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_registrate(self):
        data = {
            'Name': 'Скибиди',
            'Surname': 'Туалет',
            'Patronymic': 'Андреевич',
            'Email': '.@.',
            'Birthday': '2000-12-04',
            'TG_ID': '15'
        }
        data = json.dumps(data)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(People.objects.all()), 1)

    def test_registrate_same(self):
        data = {
            'Name': 'Скибиди',
            'Surname': 'Туалет',
            'Patronymic': 'Андреевич',
            'Email': '.@.',
            'Birthday': '2000-12-04',
            'TG_ID': '15'
        }
        data = json.dumps(data)
        response = self.client.post(self.url, data, content_type='application/json')
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.json()['status'], 'failure')
        self.assertEqual(len(People.objects.all()), 1)

    def test_registrate_second(self):
        data1 = {
            'Name': 'Скибиди',
            'Surname': 'Туалет',
            'Patronymic': 'Андреевич',
            'Email': '.@.',
            'Birthday': '2000-12-04',
            'TG_ID': '15'
        }
        data2 = {
            'Name': 'Фортенайте',
            'Surname': 'ЫЛЫ',
            'Patronymic': 'ПаБаДЖи',
            'Email': 'ПабаДЖы@.',
            'Birthday': '2000-12-04',
            'TG_ID': '17'
        }

        response = self.client.post(self.url, data1, content_type='application/json')
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(People.objects.all()), 1)

        response = self.client.post(self.url, data2, content_type='application/json')
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(People.objects.all()), 2)

class POSTanswersTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/answers_d4266fadaf6b4d8d557160643324a1d9470a5dc0ad973784f553b6918fc4a619'

        fillQuestions('', flag=True)

        People.objects.create(
            Name='Фортенайте',
            Surname='ЫЛЫ',
            Patronymic='ПаБаДЖи',
            Email='ПабаДЖы@.',
            Birthday='2000-12-04',
            TG_ID='17'
        )


    def test_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_answer_with_empty_TG_ID(self):
        json_path = os.path.join(BASE_DIR, "Utils/answers.json")
        with open(json_path, 'r') as f:
            data = json.load(f)
            del data['TG_ID']

            response = self.client.post(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['status'], 'DB has not changed')

    def test_answer_with_invalid_TG_ID(self):
        json_path = os.path.join(BASE_DIR, "Utils/answers.json")
        with open(json_path, 'r') as f:
            data = json.load(f)
            data['TG_ID'] = '71' # valid is 17

            response = self.client.post(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['status'], 'DB has not changed')

    def test_answer_with_valid_TG_ID(self):
        json_path = os.path.join(BASE_DIR, "Utils/answers.json")
        with open(json_path, 'r') as f:
            data = json.load(f)
            data['TG_ID'] = '17'

            response = self.client.post(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['status'], 'inserted')


class GETstatisticsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/statistics_26a73614cf8dd8f7aeffec47fef1b6201896ece31e52a0c706ad5b7513f7851a'

        fillQuestions('', flag=True)

        People.objects.create(
            Name='Фортенайте',
            Surname='ЫЛЫ',
            Patronymic='ПаБаДЖи',
            Email='ПабаДЖы@.',
            Birthday='2000-12-04',
            TG_ID='17'
        )

        json_path = os.path.join(BASE_DIR, "Utils/answers.json")
        with open(json_path, 'r') as f:
            data = json.load(f)
            data['TG_ID'] = '17'

            response = self.client.post(
                f'{API_ADDRESS}/answers_d4266fadaf6b4d8d557160643324a1d9470a5dc0ad973784f553b6918fc4a619',
                data,
                content_type='application/json'
            )

    def test_method_not_allowed(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_statistics_empty_TG_ID(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'Some problems with TG_ID')

    def test_statistics_invalid_TG_ID(self):
        response = self.client.get(self.url, {'TG_ID': '71'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'Some problems with TG_ID')

    def test_statistics_valid_TG_ID(self):
        response = self.client.get(self.url, {'TG_ID': '17'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)


class GETcheckPeopleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/check_people_0bb97721ff2c77036c66e6953a6ea632a424e36e6730fe74df52e3bbe6fcfa66'

        People.objects.create(
            Name='Фортенайте',
            Surname='ЫЛЫ',
            Patronymic='ПаБаДЖи',
            Email='ПабаДЖы@.',
            Birthday='2000-12-04',
            TG_ID='17'
        )

    def test_method_not_allowed(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_empty_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['isTherePeople'], 'Needs TG_ID field')

    def test_existing_people(self):
        response = self.client.get(self.url, {'TG_ID': '17'})
        self.assertEqual(response.json()['isTherePeople'], True)

    def test_non_existing_people(self):
        response = self.client.get(self.url, {'TG_ID': '71'})
        self.assertEqual(response.json()['isTherePeople'], False)