from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from users.models import Expert, Company
from users.forms import *


class TestUserViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout_user')
        self.registration_url = reverse('users:registration')
        self.expert = Expert.objects.create(email='expert@example.com', first_name='John', last_name='Doe')
        self.expert.set_password('test123')
        self.company = Company.objects.create(email='company@example.com', name='John')
        self.expert.set_password('test123')
        self.admin = User.objects.create_superuser(username='admin_test')
        self.admin.set_password('complex_password')
        self.expert.save()

    def test_logout_expert(self):
        self.client.login(email='expert@example.com', password='complex_password')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertEqual(response.status_code, 302)

    def test_logout_company(self):
        self.client.login(email='company@example.com', password='complex_password')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertEqual(response.status_code, 302)

    def test_logout_admin(self):
        self.client.login(username='admin_test', password='complex_password')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.login_url)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertEqual(response.status_code, 302)

    def test_login_view_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_view_POST_valid_credentials_expert(self):
        response = self.client.post(self.login_url, {'email': 'expert@example.com', 'password': 'test123'})
        self.assertRedirects(response, reverse('segmentation:project_show'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)

    def test_login_view_POST_invalid_credentials(self):
        response = self.client.post(self.login_url, {'email': 'expert@example.com', 'password': 'wrongpassword'})
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, 'Неверно введён пароль или логин! Или такого пользователя не существует')

    def test_login_view_POST_valid_credentials_admin(self):
        # Create a Company user
        user = User.objects.create_superuser(username='admin', email='admin@example.com', )
        user.set_password('test123')
        user.save()
        response = self.client.post(self.login_url, {'email': 'admin@example.com', 'password': 'test123'})
        self.assertRedirects(response, reverse('admin:index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)

    def test_registration_view_get(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertIsInstance(response.context['expert_form'], RegistrationExpertForm)
        self.assertIsInstance(response.context['company_form'], RegistrationCompanyForm)

    def test_str_company(self):
        self.assertEqual(self.company.__str__(), 'John')

    def test_registration_view_post_expert(self):
        post_data = {
            'role': 'expert',
            'email': 'expert@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'complex_password',
            'password2': 'complex_password'
        }
        response = self.client.post(self.registration_url, data=post_data)
        self.assertEqual(response.status_code, 200)  # Render checkCode.html
        self.assertTrue(Expert.objects.filter(email='expert@example.com').exists())

    def test_registration_view_post_expert_invalid(self):
        post_data = {
            'role': 'expert',
            'email': 'invalid-email',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'complex_password',
            'password2': 'complex_password'
        }
        response = self.client.post(self.registration_url, data=post_data)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertFalse(Expert.objects.filter(email='invalid-email').exists())
        self.assertContains(response, 'Ошибка регистрации')

    def test_registration_view_post_company(self):
        post_data = {
            'role': 'company',
            'email': 'company@example.com',
            'name': 'Example Company',
            'password1': 'complex_password',
            'password2': 'complex_password'
        }
        response = self.client.post(self.registration_url, data=post_data)
        self.assertEqual(response.status_code, 200)  # Render checkCode.html
        self.assertTrue(Company.objects.filter(email='company@example.com').exists())

    def test_registration_view_post_company_invalid(self):
        post_data = {
            'role': 'company',
            'email': 'invalid-email',
            'name': 'Example Company',
            'password1': 'complex_password',
            'password2': 'complex_password'
        }
        response = self.client.post(self.registration_url, data=post_data)
        self.assertEqual(response.status_code, 200)  # Should stay on the same page
        self.assertFalse(Company.objects.filter(email='invalid-email').exists())
        self.assertContains(response, 'Ошибка регистрации')
