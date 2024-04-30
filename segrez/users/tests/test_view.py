from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from users.models import Expert, Company

class TestUserViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.expert = Expert.objects.create(email='expert@example.com', first_name='John', last_name='Doe')
        self.expert.set_password('test123')
        self.expert.save()

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
        self.assertContains(response, 'Неверно введёт пароль или логин!')

    def test_login_view_POST_valid_credentials_admin(self):
        # Create a Company user
        user = User.objects.create_superuser(username='admin', email='admin@example.com', )
        user.set_password('test123')
        user.save()
        response = self.client.post(self.login_url, {'email': 'admin@example.com', 'password': 'test123'})
        self.assertRedirects(response, reverse('admin:index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.status_code, 302)
