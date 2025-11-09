from django import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Имя пользователя')
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text='Пароль должен содержать не менее 8 символов.'
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        help_text='Введите тот же пароль, что и выше, для подтверждения.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'phone', 'email', 'message']  # Убрана 'service'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Сообщение', 'rows': 4}),
        }
