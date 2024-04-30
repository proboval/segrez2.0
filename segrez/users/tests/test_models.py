from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Company, Expert


class CompanyModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create_user(email='test@example.com', name='Test Company', password='test123')

    def test_create_user(self):
        self.assertTrue(isinstance(self.company, Company))
        self.assertEqual(self.company.email, 'test@example.com')
        self.assertEqual(self.company.name, 'Test Company')
        self.assertTrue(self.company.check_password('test123'))

    def test_required_fields(self):
        with self.assertRaises(ValueError):
            Company.objects.create_user(email='', name='Test Company', password='test123')


class ExpertModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create_user(email='company@example.com', name='Company', password='company123')
        self.expert = Expert.objects.create_user(email='expert@example.com', first_name='John', last_name='Doe', password='test123', company=self.company)

    def test_create_user(self):
        self.assertTrue(isinstance(self.expert, Expert))
        self.assertEqual(self.expert.email, 'expert@example.com')
        self.assertEqual(self.expert.first_name, 'John')
        self.assertEqual(self.expert.last_name, 'Doe')
        self.assertEqual(self.expert.company, self.company)
        self.assertTrue(self.expert.check_password('test123'))

    def test_required_fields(self):
        with self.assertRaises(ValueError):
            Expert.objects.create_user(email='', first_name='John', last_name='Doe', password='test123')
