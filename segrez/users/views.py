from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import RegistrationExpertForm, RegistrationCompanyForm, LoginUserForm, checkEmailForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth import logout
from django.db import transaction


def logout_user(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect(reverse('users:login'))


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if type(user) in [type(Expert()), type(Company())]:
                messages.success(request, 'Вы успешно авторизовались')
                return redirect(reverse('segmentation:project_show'))
            else:
                messages.success(request, 'Вы успешно авторизовались!')
                return redirect('admin:index')
        else:
            messages.error(request, 'Неверно введён пароль или логин! Или такого пользователя не существует')

    form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        if request.POST['role'] == 'expert':
            expert_form = RegistrationExpertForm(request.POST)
            company_form = RegistrationCompanyForm()
            if expert_form.is_valid():
                expert = expert_form.save()
                context = {'pk': expert.pk, 'form': checkEmailForm(), 'role': request.POST['role']}
                response = redirect(reverse('users:checkCode'))
                response.set_cookie('pk', expert.pk)
                response.set_cookie('role', request.POST['role'])
                messages.success(request, f'Проверьте почту {expert.email}')
                print('Вывод формы для проверки пароля')
                return response
            else:
                messages.error(request, 'Ошибка регистрации')
        elif request.POST['role'] == 'company':
            expert_form = RegistrationExpertForm()
            company_form = RegistrationCompanyForm(request.POST)
            if company_form.is_valid():
                company = company_form.save()
                context = {'pk': company.pk, 'form': checkEmailForm(), 'role': request.POST['role']}
                messages.success(request, f'Проверьте почту {company.email}')
                return render(request, 'users/checkCode.html', context)
            else:
                messages.error(request, 'Ошибка регистрации')
    else:
        expert_form = RegistrationExpertForm()
        company_form = RegistrationCompanyForm()

    return render(request, 'users/registration.html', {'expert_form': expert_form,
                                                       'company_form': company_form})


def checkCode_view(request):
    print('запустилося')
    if request.method == 'POST':
        print(request.POST)
        form = checkEmailForm(request.POST)
        if form.is_valid():
            print('форма заполнена')
            code = request.POST.get('code')
            pk = request.COOKIES['pk']
            role = request.COOKIES['role']

            if role == 'company':
                user = Company.objects.get(pk=pk)
            else:
                user = Expert.objects.get(pk=pk)

            if user.secretcode == code:
                user.is_active = True
                user.secretcode = None
                user.save()
                messages.success(request, 'Регистрация завершена успешно!')
                return redirect(reverse('users:login'))
            else:
                messages.error(request, 'Введен неверный код!')

    return render(request, 'users/checkCode.html', {'form' : checkEmailForm()})


@csrf_exempt
def cancelRegistration(request):
    if request.method == 'POST':
        pk = request.COOKIES['pk']
        role = request.COOKIES['role']

        with transaction.atomic():
            if role == 'company':
                company = Company.objects.get(pk=pk).delete()
            else:
                expert = Expert.objects.get(pk=pk).delete()

        return JsonResponse({'message': 'Данные успешно удалены'})
    else:
        return JsonResponse({'error': 'Ошибка'})
