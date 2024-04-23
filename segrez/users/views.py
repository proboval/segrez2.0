from django.shortcuts import render, redirect
from .forms import RegistrationExpertForm, RegistrationCompanyForm, LoginUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth import logout


def logout_user(request):
    logout(request)
    return redirect(reverse('users:login'))


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно авторизовались')
            if type(user) in [type(Expert()), type(Company())]:
                return redirect(reverse('segmentation:project_show'))
            else:
                return redirect('admin:index')
        else:
            messages.error(request, 'Неверно введёт пароль или логин! Или такого пользователя не существует')

    form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        if request.POST['role'] == 'expert':
            expert_form = RegistrationExpertForm(request.POST)
            company_form = RegistrationCompanyForm()
            if expert_form.is_valid():
                expert_form.save()
                messages.success(request, 'Вы успешно зарегистрировались как эксперт!')
                return redirect('login')
            else:
                messages.error(request, 'Ошибка регистрации')
        elif request.POST['role'] == 'company':
            expert_form = RegistrationExpertForm()
            company_form = RegistrationCompanyForm(request.POST)
            if company_form.is_valid():
                company_form.save()
                messages.success(request, 'Вы успешно зарегистрировались как компания!')
                return redirect(reverse('users:login'))
            else:
                messages.error(request, 'Ошибка регистрации')
    else:
        expert_form = RegistrationExpertForm()
        company_form = RegistrationCompanyForm()

    return render(request, 'users/registration.html', {'expert_form': expert_form, 'company_form': company_form})
