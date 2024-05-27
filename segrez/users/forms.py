from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from random import randint
from .models import Company, Expert
from django.core.mail import send_mail


class addUserForm(forms.Form):
    pk = forms.CharField(label='ID эксперта', widget=forms.TextInput(attrs={'class': 'form-control'}))


class checkEmailForm(forms.Form):
    code = forms.CharField(label='Код', widget=forms.TextInput(attrs={'class': 'form-control'}))


class LoginUserForm(forms.Form):
    email = forms.EmailField(label='Почта',
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegistrationExpertForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=25)
    last_name = forms.CharField(label='Фамилия', max_length=25)
    email = forms.EmailField(label='Почта')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        emailExpert = Expert.objects.filter(email=email)
        emailCompany = Company.objects.filter(email=email)
        emailUser = User.objects.filter(email=email)
        print(emailUser)
        if emailExpert.count() or emailCompany.count() or emailUser.count():
            print('проблема с почтой')
            raise ValidationError("Пользователь с такой почтой уже существует")
        print('проблемы с почтой нет')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        print('вызван')
        if password1 and password2 and password1 != password2:
            print('проблема')
            raise ValidationError("Пароли не совпадают")
        print('проблемы нет')
        return password2

    class Meta:
        model = Expert
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        secretCode = randint(1, 10000)
        secretCode = '0' * (4 - len(str(secretCode))) + str(secretCode)

        expert = Expert.objects.create_user(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                password=self.cleaned_data['password1'],
                secretcode=secretCode,
                is_active=False,
               )

        subject = 'Регистрация на платформе Segrez'
        message = f'Здравствуйте, {expert.last_name} {expert.first_name}!\nКод для регистрации в SegRez: {secretCode}.'

        send_mail(subject=subject, message=message, from_email='SegRez@yandex.ru', recipient_list=[expert.email,],
                  fail_silently=False)

        return expert


class RegistrationCompanyForm(UserCreationForm):
    name = forms.CharField(label='Название компании', max_length=25)
    email = forms.EmailField(label='Почта')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        emailExpert = Expert.objects.filter(email=email)
        emailCompany = Company.objects.filter(email=email)
        emailUser = User.objects.filter(email=email)
        if emailExpert.count() or emailCompany.count() or emailUser.count():
            raise ValidationError("Пользователь с такой почтой уже существует")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        print('вызван')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    class Meta:
        model = Company
        fields = ('name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        secretCode = randint(1, 10000)
        secretCode = '0' * (4 - len(str(secretCode))) + str(secretCode)

        сompany = Company.objects.create_user(
                name=self.cleaned_data['name'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password1'],
                secretcode=secretCode,
                is_active=False,
               )

        subject = 'Регистрация на платформе Segrez'
        message = f'Здравствуйте, {сompany.name}!\nКод для регистрации в SegRez: {secretCode}.'

        send_mail(subject=subject, message=message, from_email='SegRez@yandex.ru', recipient_list=[сompany.email, ],
                  fail_silently=False)

        return сompany
