from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Service, Booking
from .forms import BookingForm
import telegram


def booking_form(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
            bot.send_message(
                chat_id='твой_chat_id',
                text=f'Новая запись: {booking.name}, {booking.phone}, {booking.email}'
            )
            return JsonResponse({'success': True})


def home(request):
    services = Service.objects.filter(is_active=True)
    form = BookingForm()
    return render(request, 'pages/home.html', {
        'services': services,
        'form': form
    })


def booking_form(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Пожалуйста, заполните все поля корректно'})

    return JsonResponse({'success': False, 'error': 'Метод не разрешён'})
