import json
import os

from django.test import TestCase, Client
from freezegun import freeze_time

from .models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_ADDRESS = os.path.join(BASE_DIR, "Utils/answers.json")
API_ADDRESS = '/django/api'

# Create your tests here.
class GETquestionsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/questions_368c231b7c9a3d506cef5a936c83d92f068179d849db19ac2608ba288c7c1c56'
        self.url_reg = f'{API_ADDRESS}/registration_8d6238094a7742ac22fedb3a180bc590d35f5ea70b8a262cc0bd976349b6181d'
        self.url_test = f'{API_ADDRESS}/answers_d4266fadaf6b4d8d557160643324a1d9470a5dc0ad973784f553b6918fc4a619'

        data = {
            'Nickname': 'Фортенайте',
            'Email': 'ПабаДЖы@.',
            'Work_Experience': '1',
            'Birthday': '2000-12-04',
            'TG_ID': '17'
        }

        self.client.post(self.url_reg, data, content_type='application/json')


    def test_method_not_allowed(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_get_data_without_TG_ID(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get_data_with_invalid_TG_ID(self):
        response = self.client.get(self.url, {'TG_ID': '71'})
        self.assertEqual(response.status_code, 401)

    def test_get_data(self):
        response = self.client.get(self.url, {'TG_ID': '17'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 84)
        self.assertEqual(response.json()[0]['Name_Question'], 'Организационные недостатки на работе постоянно заставляют нервничать, переживать, напрягаться.')
        self.assertEqual(len(response.json()[1]), 2)

    def test_get_data_with_active_test(self):
        json_path = JSON_ADDRESS
        with open(json_path, 'r') as f:
            data = json.load(f)
            data['TG_ID'] = '17'
            self.client.post(self.url_test, data, content_type='application/json')

        response = self.client.get(self.url, {'TG_ID': '17'})
        self.assertEqual(response.status_code, 403)

    @freeze_time("2025-08-01")
    def test_get_data_without_active_test(self):
        json_path = JSON_ADDRESS
        with open(json_path, 'r') as f:
            data = json.load(f)
            data['TG_ID'] = '17'
            self.client.post(self.url_test, data, content_type='application/json')

        with freeze_time("2025-09-15"):
            response = self.client.get(self.url, {'TG_ID': '17'})
            self.assertEqual(response.status_code, 200)

class POSTregistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/registration_8d6238094a7742ac22fedb3a180bc590d35f5ea70b8a262cc0bd976349b6181d'

    def test_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_registrate(self):
        data = {
            'Nickname': 'Фортенайте',
            'Email': 'ПабаДЖы@.',
            'Work_Experience': '1',
            'Birthday': '2000-12-04',
            'TG_ID': '17'
        }
        data = json.dumps(data)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(People.objects.all()), 1)

    def test_registrate_with_empty_fields(self):
        data = {
            'Nickname': 'ПаБаДЖИ',
            'Email': '',
            'Work_Experience': '1',
            'Birthday': '2000-12-04',
            'TG_ID': '18'
        }
        data = json.dumps(data)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(People.objects.all()), 1)

    def test_registrate_same(self):
        data = {
            'Nickname': 'Фортенайте',
            'Email': '',
            'Work_Experience': '1',
            'Birthday': '2000-12-04',
            'TG_ID': '17'
        }
        data = json.dumps(data)
        response = self.client.post(self.url, data, content_type='application/json')
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.json()['status'], 'TG_ID or Nickname exists')
        self.assertEqual(len(People.objects.all()), 1)

    def test_registrate_second(self):
        data1 = {
            'Nickname': 'Фортенайте',
            'Email': '',
            'Work_Experience': '1',
            'Birthday': '2000-12-04',
            'TG_ID': '17'
        }
        data2 = {
            'Nickname': 'ПАБАДЖИ',
            'Email': '',
            'Work_Experience': '1',
            'Birthday': '2000-12-04',
            'TG_ID': '18'
        }

        response = self.client.post(self.url, data1, content_type='application/json')
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(People.objects.all()), 1)

        response = self.client.post(self.url, data2, content_type='application/json')
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(People.objects.all()), 2)

    def test_registrate_second_with_nickname(self):
        data = {
            'Nickname': 'Фортенайте',
            'Email': 'ПабаДЖы@.',
            'Work_Experience': '1',
            'Birthday': '2000-12-04',
            'TG_ID': '71'
        }

        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(People.objects.all()), 1)

class GETcheckNicknameTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/check_nickname_4b4f04bfd927c2a6381a392dcfedcd258e7dfb6e0401f674b13bc4c0db01bcb5'

        People.objects.create(
            Nickname='Фортенайте',
            Email='ПабаДЖы@.',
            Work_Experience='1',
            Birthday='2000-12-04',
            TG_ID='17'
        )

    def test_existing_nickname(self):
        response = self.client.get(self.url, {'Nickname': 'Фортенайте'})
        self.assertEqual(response.json()['status'], 'exists')

    def test_unextisting_nickname(self):
        response = self.client.get(self.url, {'Nickname': 'ИЛЫ_ПАБАДЖИ'})
        self.assertEqual(response.json()['status'], 'does not exist')


class POSTanswersTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/answers_d4266fadaf6b4d8d557160643324a1d9470a5dc0ad973784f553b6918fc4a619'

        People.objects.create(
            Nickname='Фортенайте',
            Email='ПабаДЖы@.',
            Work_Experience='1',
            Birthday='2000-12-04',
            TG_ID='17'
        )


    def test_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_answer_with_empty_TG_ID(self):
        json_path = JSON_ADDRESS
        with open(json_path, 'r') as f:
            data = json.load(f)
            del data['TG_ID']

            response = self.client.post(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['status'], 'DB has not changed')

    def test_answer_with_invalid_TG_ID(self):
        json_path = JSON_ADDRESS
        with open(json_path, 'r') as f:
            data = json.load(f)
            data['TG_ID'] = '71' # valid is 17

            response = self.client.post(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['status'], 'DB has not changed')

    def test_answer_with_valid_TG_ID(self):
        json_path = JSON_ADDRESS
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

        People.objects.create(
            Nickname='Фортенайте',
            Email='ПабаДЖы@.',
            Work_Experience='1',
            Birthday='2000-12-04',
            TG_ID='17'
        )

        json_path = JSON_ADDRESS
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
            Nickname='Фортенайте',
            Email='ПабаДЖы@.',
            Work_Experience='1',
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


def addBurnoutTest(client):
    json_path = JSON_ADDRESS
    with open(json_path, 'r') as f:
        data = json.load(f)
        data['TG_ID'] = '17'

        response = client.post(
            f'{API_ADDRESS}/answers_d4266fadaf6b4d8d557160643324a1d9470a5dc0ad973784f553b6918fc4a619',
            data,
            content_type='application/json'
        )


class EvereweekTasksTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/everyweek_tasks_4a73556cb2e8ca050437f3868dccef0cee3bb02b5beb1b8d46882a43e452522e'

        People.objects.create(
            Nickname='Фортенайте',
            Email='ПабаДЖы@.',
            Work_Experience='1',
            Birthday='2000-12-04',
            TG_ID='17'
        )

    def test_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

        response = self.client.post(self.url, {}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.patch(self.url, {}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.delete(self.url, {}, content_type='application/json')
        self.assertEqual(response.status_code, 405)

    def test_get_tasks_with_no_tests(self):
        data = {
            'TG_ID': '17'
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['status'], 'There are no tests')

    @freeze_time("2025-08-01")
    def test_get_tasks_with_old_tests(self):
        addBurnoutTest(self.client)

        data = {
            'TG_ID': '17'
        }
        with freeze_time("2025-10-01"):
            response = self.client.get(self.url, data)
            self.assertEqual(response.status_code, 410)
            self.assertEqual(response.json()['status'], 'The test was a long time ago')

    def test_get_tasks_with_new_tests(self):
        addBurnoutTest(self.client)

        data = {
            'TG_ID': '17'
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json()['took_tasks'], [])

    def test_post_empty_TG_ID(self):
        response = self.client.post(self.url, {}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_invalid_TG_ID(self):
        data = {
            'TG_ID': 'brrr',
            'TaskID': ''
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['status'], f'There is no such people with such TG_ID: {data["TG_ID"]}')

    def test_post_no_tests(self):
        data = {
            'TG_ID': '17',
            'TaskID': ''
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['status'], f'There are no tests yet')

    @freeze_time("2025-08-01")
    def test_post_tasks_with_old_tests(self):
        addBurnoutTest(self.client)

        data = {
            'TG_ID': '17',
            'TaskID': '1',
        }
        with freeze_time("2025-10-01"):
            response = self.client.post(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, 410)
            self.assertEqual(response.json()['status'], 'The test was a long time ago')

    def test_post_new_task(self):
        addBurnoutTest(self.client)

        data = {
            'TG_ID': '17',
            'TaskID': '1',
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_new_task_with_unclosed_one(self):
        addBurnoutTest(self.client)

        data = {
            'TG_ID': '17',
            'TaskID': '1',
        }
        self.client.post(self.url, data, content_type='application/json')

        data = {
            'TG_ID': '17',
            'TaskID': '2',
        }
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_patch_not_from_1_to_5_stars(self):
        addBurnoutTest(self.client)

        data = {
            'TG_ID': '17',
            'TaskID': '1',
        }
        self.client.post(self.url, data, content_type='application/json')

        data = {
            'TG_ID': '17',
            'Stars': '0',
            'Comments': '',
        }
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = {
            'TG_ID': '17',
            'Stars': '100500',
            'Comments': '',
        }
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_patch_waiting_a_week(self):
        addBurnoutTest(self.client)

        data = {
            'TG_ID': '17',
            'TaskID': '1',
        }
        self.client.post(self.url, data, content_type='application/json')

        data = {
            'TG_ID': '17',
            'Stars': '5',
            'Comments': 'Билибоба',
        }
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    @freeze_time("2025-08-01")
    def test_patch_update_stars_and_trying_second_update(self):
        addBurnoutTest(self.client)

        data = {
            'TG_ID': '17',
            'TaskID': '1',
        }
        self.client.post(self.url, data, content_type='application/json')

        data = {
            'TG_ID': '17',
            'Stars': '5',
            'Comments': 'Билибоба',
        }
        with freeze_time("2025-08-09"):
            response = self.client.patch(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, 200)

            response = self.client.patch(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, 403)


class OptionsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/options_33eafc9c4333dc5ecbe984d3b75cc9a683a3f86f143bb5ed68607947f5c20a19'

        People.objects.create(
            Nickname='Фортенайте',
            Email='ПабаДЖы@.',
            Work_Experience='1',
            Birthday='2000-12-04',
            TG_ID='17'
        )

    def test_get_empty_TG_ID(self):
        response = self.client.get(self.url, {}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_invalid_TG_ID(self):
        data = {
            'TG_ID': 'brrr',
        }
        response = self.client.get(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['status'], f'There is no such people with such TG_ID: {data["TG_ID"]}')

    def test_get_existing_TG_ID(self):
        data = {
            'TG_ID': '17',
        }
        response = self.client.get(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_patch_missing_tg_id(self):
        response = self.client.patch(self.url, {}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'TG_ID is required')

    def test_patch_invalid_tg_id(self):
        data = {"TG_ID": "999"}
        response = self.client.patch(self.url, data, content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("There is no such people", response.json()['status'])

    def test_patch_invalid_field(self):
        data = {"TG_ID": "17", "KEK": "LOL"}
        response = self.client.patch(self.url, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Field KEK is not allowed", response.json()['status'])

    def test_patch_update_email(self):
        data = {"TG_ID": "17", "Email": "NotSkibidi@mail.com"}
        response = self.client.patch(self.url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'Updated')
        person = People.objects.filter(TG_ID=17).first()
        self.assertEqual(person.Email, "NotSkibidi@mail.com")

    def test_patch_update_options_field(self):
        data = {"TG_ID": "17", "Notification_Day": "False"}
        response = self.client.patch(self.url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        options = People.objects.filter(TG_ID=17).first().options
        self.assertEqual(options.Notification_Day, False)


class EverydayAnswersTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/everyday_answers_7f5831436bc60af14dd1d0c9a4d09f73092a2560d9d1e6d28eba22e6d9effce8'

        self.person = People.objects.create(
            Nickname='Фортенайте',
            Email='ПабаДЖы@.',
            Work_Experience='1',
            Birthday='2000-12-04',
            TG_ID='17'
        )

    def test_get_can_i_send_test_true(self):
        response = self.client.get(self.url, {'TG_ID': '17'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Can I send the answer'], 'True')

    def test_get_can_i_send_test_false(self):
        Answers_Everyday.objects.create(
            People_ID=self.person,
            Emotional_Condition=1,
            Physical_Condition=1,
            Burnout=1,
        )

        response = self.client.get(self.url, {'TG_ID': '17'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['Can I send the answer'], 'False')

    @freeze_time("2025-08-01")
    def test_get_can_i_send_test_true_after_a_day(self):
        Answers_Everyday.objects.create(
            People_ID=self.person,
            Emotional_Condition=1,
            Physical_Condition=1,
            Burnout=1,
        )

        with freeze_time("2025-08-02"):
            response = self.client.get(self.url, {'TG_ID': '17'}, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['Can I send the answer'], 'True')

    def test_post_success(self):
        data = {
            "TG_ID": "17",
            "Answers": {
                "Emotional_Condition": 2,
                "Physical_Condition": 3,
                "Burnout": 1
            }
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.json()["status"], "added")
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Answers_Everyday.objects.count(), 1)

    def test_post_person_not_found(self):
        data = {
            "TG_ID": "999",
            "Answers": {
                "Emotional_Condition": 2,
                "Physical_Condition": 3,
                "Burnout": 1
            }
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 404)
        self.assertIn("There is no such people", response.json()["status"])

    @freeze_time("2025-08-01 10:00:00")
    def test_post_already_answered_today(self):
        Answers_Everyday.objects.create(
            People_ID=self.person,
            Emotional_Condition=2,
            Physical_Condition=2,
            Burnout=2,
        )

        data = {
            "TG_ID": "17",
            "Answers": {
                "Emotional_Condition": 1,
                "Physical_Condition": 1,
                "Burnout": 1
            }
        }
        with freeze_time("2025-08-01 11:00:00"):
            response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")

            self.assertEqual(response.status_code, 403)
            self.assertEqual(response.json()["status"], "There was today's answer")

    def test_post_missing_fields(self):
        data = {
            "TG_ID": "17",
            "Answers": {
                "Emotional_Condition": 1,
                "Physical_Condition": 2
                # There is no Burnout
            }
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("are required", response.json()["status"])

    def test_post_invalid_values(self):
        data = {
            "TG_ID": "17",
            "Answers": {
                "Emotional_Condition": 5,
                "Physical_Condition": 0,
                "Burnout": -1
            }
        }
        response = self.client.post(self.url, data=json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("conditions must be in [1, 3]", response.json()["status"])


class EverydayAnswersStatisticsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f'{API_ADDRESS}/statistics_everyday_answers_c23820a3029e86a952fb596d5ac69ec7f5306625732ada45b7c09f926237728a'

        self.person = People.objects.create(
            Nickname='Фортенайте',
            Email='ПабаДЖы@.',
            Work_Experience='1',
            Birthday='2000-12-04',
            TG_ID='17'
        )

        Answers_Everyday.objects.create(
            People_ID=self.person,
            Emotional_Condition=3,
            Physical_Condition=3,
            Burnout=3,
        )

    def test_method_not_allowed(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_statistics_empty_TG_ID(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['status'], 'Needs TG_ID field')

    def test_statistics_invalid_TG_ID(self):
        response = self.client.get(self.url, {'TG_ID': '71'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['status'], f'There is no person with this 71 TG_ID')

    def test_statistics_valid_TG_ID(self):
        response = self.client.get(self.url, {'TG_ID': '17'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

