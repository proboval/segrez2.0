import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import *
from django.urls import reverse
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


def addUser(request):
    if request.method == 'POST':
        form = addUserForm(request.POST)
        if form.is_valid():
            expert_pk = request.POST.get('pk')
            expert = None
            if Expert.objects.filter(pk=expert_pk).exists():
                expert = Expert.objects.get(pk=expert_pk)
            if expert:
                if expert.company is None:
                    expert.company = request.user
                    expert.save()

                    subject = 'Приглашение в компанию'
                    message = (f'Здравствуйте, {expert.last_name} {expert.first_name}!\n'
                               f'Вас только что добавили в компанию {request.user}.\n')
                    send_mail(subject=subject, message=message, from_email='SegRez@yandex.ru',
                              recipient_list=[expert.email],
                              fail_silently=False)

                    messages.success(request, f'{expert} успешно добавлен в компанию')
                else:
                    messages.error(request, f'{expert} уже состоит в компании')
                return redirect(reverse('segmentation:project_show'))
            else:
                messages.error(request, 'Пользователя с данным ключом не существует')

    return render(request, 'users/addUser.html', {'form': addUserForm()})


@csrf_exempt
def removeExpertFromCompany(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        expertId = int(data.get('expertId'))
        expert = Expert.objects.get(pk=expertId)
        subject = 'Удаление из компании'
        message = (f'Здравствуйте, {expert.last_name} {expert.first_name}!\n'
                   f'Вас только что удалили из компании {request.user}.\n'
                   f'Для уточнения причин обратитесь по почте {request.user.email}.')
        send_mail(subject=subject, message=message, from_email='SegRez@yandex.ru', recipient_list=[expert.email],
                  fail_silently=False)
        expert.company = None
        expert.save()
    print('переход')
    return redirect(reverse('segmentation:project_show'))
