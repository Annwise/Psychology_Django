from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, Booking
from .forms import BookingForm

def home(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'pages/home.html', {'services': services})

def booking_form(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            messages.success(request, 'Спасибо за запись! Мы свяжемся с вами в ближайшее время.')
            return redirect('home')
    else:
        form = BookingForm()
    
    services = Service.objects.filter(is_active=True)
    return render(request, 'pages/booking_form.html', {
        'form': form,
        'services': services
    })
