from django.shortcuts import render, redirect
from .forms import RegistrationExpertForm, RegistrationCompanyForm
from django.contrib import messages


def registration_view(request):
    if request.method == 'POST':
        expert_form = RegistrationExpertForm(request.POST)
        company_form = RegistrationCompanyForm(request.POST)
        print(expert_form)
        if expert_form.is_valid():
            expert_form.save()
            messages.success(request, 'Вы успешно зарегистрировались как эксперт!')
            return render(request, 'users/registration.html',
                          {'expert_form': RegistrationExpertForm(), 'company_form': RegistrationCompanyForm()})
        elif company_form.is_valid():
            company_form.save()
            messages.success(request, 'Вы успешно зарегистрировались как компания!')
            return render(request, 'users/registration.html',
                          {'expert_form': RegistrationExpertForm(), 'company_form': RegistrationCompanyForm()})
        else:
            return render(request, 'users/registration.html',
                          {'expert_form': RegistrationExpertForm(), 'company_form': RegistrationCompanyForm()})
    else:
        expert_form = RegistrationExpertForm()
        company_form = RegistrationCompanyForm()
        print('24 строка')
        return render(request, 'users/registration.html', {'expert_form': expert_form, 'company_form': company_form})
