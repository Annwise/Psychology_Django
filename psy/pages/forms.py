from django import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomUserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Имя', help_text='Обязательное поле. Только буквы.')
    last_name = forms.CharField(max_length=30, label='Фамилия', help_text='Обязательное поле. Только буквы.')
    email = forms.EmailField(required=True, label='Email', help_text='Введите действительный email.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')  # ← без username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # ← автоматически
        if commit:
            user.save()
        return user


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Сообщение', 'rows': 4}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            # Используем email как username
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Неверный email или пароль.')
        return self.cleaned_data
