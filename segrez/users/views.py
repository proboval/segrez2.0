from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Company, Expert


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            if role == 'company':
                print("Create new company")
            elif role == 'expert':
                print("Create new ")
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'form': form})
