# users/tests/test_forms.py

from django.test import TestCase
from django.contrib.auth.models import User
from users.forms import addUserForm, checkEmailForm, LoginUserForm, RegistrationExpertForm, RegistrationCompanyForm
from users.models import Expert, Company
from django.core.exceptions import ValidationError


class AddUserFormTest(TestCase):

    def test_add_user_form_valid_data(self):
        form = addUserForm(data={'pk': '12345'})
        self.assertTrue(form.is_valid())

    def test_add_user_form_no_data(self):
        form = addUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class CheckEmailFormTest(TestCase):

    def test_check_email_form_valid_data(self):
        form = checkEmailForm(data={'code': '1234'})
        self.assertTrue(form.is_valid())

    def test_check_email_form_no_data(self):
        form = checkEmailForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)


class LoginUserFormTest(TestCase):

    def test_login_user_form_valid_data(self):
        form = LoginUserForm(data={'email': 'test@example.com', 'password': 'password123'})
        self.assertTrue(form.is_valid())

    def test_login_user_form_no_data(self):
        form = LoginUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class RegistrationExpertFormTest(TestCase):

    def test_registration_expert_form_valid_data(self):
        form = RegistrationExpertForm(data={
            'first_name': 'John1',
            'last_name': 'Doe1',
            'email': 'john1.doe@gmail.com',
            'password1': '!qAz@wSx',
            'password2': '!qAz@wSx'
        })
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_registration_expert_form_invalid_email(self):
        Expert.objects.create(email='john.doe@example.com', password='password123')
        form = RegistrationExpertForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_registration_expert_form_password_mismatch(self):
        form = RegistrationExpertForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password1': 'password123',
            'password2': 'password321'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class RegistrationCompanyFormTest(TestCase):

    def test_registration_company_form_valid_data(self):
        form = RegistrationCompanyForm(data={
            'name': 'Test Company',
            'email': 'company1@gmail.com',
            'password1': '!qAz@wSx',
            'password2': '!qAz@wSx'
        })
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_registration_company_form_invalid_email(self):
        Company.objects.create(email='company@example.com', password='password123')
        form = RegistrationCompanyForm(data={
            'name': 'Test Company',
            'email': 'company@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_registration_company_form_password_mismatch(self):
        form = RegistrationCompanyForm(data={
            'name': 'Test Company',
            'email': 'company@example.com',
            'password1': 'password123',
            'password2': 'password321'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
