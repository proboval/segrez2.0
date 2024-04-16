from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Company, Expert


class RegistrationExpertForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=25)
    last_name = forms.CharField(label='Фамилия', max_length=25)
    email = forms.EmailField(label='Почта')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        emailExpert = Expert.objects.filter(email=email)
        emailCompany = Company.objects.filter(email=email)
        if emailExpert.count() or emailCompany.count():
            print(ValidationError("Email Already Exist"))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            print(ValidationError("Пароли не совпадают"))
        return password2

    class Meta:
        model = Expert
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        expert = Expert.objects.create_user(
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                password=self.cleaned_data['password1'],
               )
        return expert


class RegistrationCompanyForm(UserCreationForm):
    name = forms.CharField(label='Название компании', max_length=25)
    email = forms.EmailField(label='Почта')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        emailExpert = Expert.objects.filter(email=email)
        emailCompany = Company.objects.filter(email=email)
        if emailExpert.count() or emailCompany.count():
            return ValidationError("Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    class Meta:
        model = Company
        fields = ('name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        сompany = Company.objects.create_user(
                email=self.cleaned_data['email'],
                last_name=self.cleaned_data['name'],
                password=self.cleaned_data['password1'],
               )
        return сompany
