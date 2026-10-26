from datetime import date

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Contract


class BookingForm(forms.Form):
    email = forms.EmailField(label='E-mail')


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['employee_code', 'signed_date', 'status']
        labels = {'employee_code': 'Код сотрудника', 'signed_date': 'Дата составления', 'status': 'Статус'}
        widgets = {'signed_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['signed_date'].initial = date.today()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')
