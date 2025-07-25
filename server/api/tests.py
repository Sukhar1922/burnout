from django.test import TestCase, Client
from .models import *

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
