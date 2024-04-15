from django import forms
from .models import Company, Expert


class RegistrationForm(forms.Form):
    role = forms.ChoiceField(choices=(('company', 'Company'), ('expert', 'Expert')), widget=forms.RadioSelect)
    # Поля для регистрации компании
    company_name = forms.CharField(max_length=50, required=False)
    company_email = forms.EmailField(max_length=255, required=False)
    # Поля для регистрации эксперта
    expert_name = forms.CharField(max_length=25, required=False)
    expert_last_name = forms.CharField(max_length=25, required=False)
    expert_email = forms.EmailField(max_length=255, required=False)

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        # Если выбрана роль "Company", убедитесь, что заполнены обязательные поля для компании
        if role == 'company':
            company_name = cleaned_data.get('company_name')
            company_email = cleaned_data.get('company_email')
            if not company_name or not company_email:
                raise forms.ValidationError('Please fill in all required fields for company registration.')
        # Если выбрана роль "Expert", убедитесь, что заполнены обязательные поля для эксперта
        elif role == 'expert':
            expert_name = cleaned_data.get('expert_name')
            expert_last_name = cleaned_data.get('expert_last_name')
            expert_email = cleaned_data.get('expert_email')
            if not expert_name or not expert_last_name or not expert_email:
                raise forms.ValidationError('Please fill in all required fields for expert registration.')
        return cleaned_data
