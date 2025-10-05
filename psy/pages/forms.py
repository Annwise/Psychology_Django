from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'phone', 'email', 'service', 'date', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Сообщение', 'rows': 4}),
        }
