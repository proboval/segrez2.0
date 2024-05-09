from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import logout_user, registration_view, login_view
from segmentation.views import project_show


class TestUserUrls(SimpleTestCase):
    def test_logout_url_is_resolved(self):
        url = reverse('users:logout_user')
        self.assertEqual(resolve(url).func, logout_user)

    def test_registration_url_is_resolved(self):
        url = reverse('users:registration')
        self.assertEqual(resolve(url).func, registration_view)

    def test_login_url_is_resolved(self):
        url = reverse('users:login')
        self.assertEqual(resolve(url).func, login_view)
