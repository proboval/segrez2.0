from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponseRedirect


class TestIndexView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'segrez/index.html')