from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import Service, Booking, PrivacyPolicy, ConsentForm
from .forms import BookingForm
import telegram


def home(request):
    services = Service.objects.filter(is_active=True)
    form = BookingForm()
    return render(request, 'pages/home.html', {
        'services': services,
        'form': form
    })


async def send_telegram_message(chat_id, text):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)


def booking_form(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Добавь обязательные поля
            booking.privacy_policy = PrivacyPolicy.objects.first()
            booking.consent_form = ConsentForm.objects.first()
            booking.accepted_privacy_policy = True
            booking.accepted_consent = True

            booking.save()

            # Отправка уведомления в Telegram
            try:
                import asyncio
                asyncio.run(send_telegram_message('705925519', f'Новая запись: {booking.name}, {booking.phone}, {booking.email}'))
            except Exception as e:
                print(f'Ошибка отправки в Telegram: {e}')

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Пожалуйста, заполните все поля корректно'})

    return JsonResponse({'success': False, 'error': 'Метод не разрешён'})


def privacy_policy(request):
    policy = PrivacyPolicy.objects.last()
    return render(request, 'pages/privacy.html', {'policy': policy})


def consent_form(request):
    consent = ConsentForm.objects.last()
    return render(request, 'pages/consent.html', {'consent': consent})
