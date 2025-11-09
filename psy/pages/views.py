from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import Service, Booking, PrivacyPolicy, ConsentForm
from .forms import BookingForm, CustomUserRegisterForm, CustomAuthenticationForm
import telegram
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages


def home(request):
    services = Service.objects.filter(is_active=True)
    form = BookingForm()
    return render(request, 'pages/home.html', {
        'services': services,
        'form': form
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('first_name')
            messages.success(request, f'Аккаунт {username} создан!')
            login(request, user)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserRegisterForm()
    return render(request, 'pages/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})


async def send_telegram_message(chat_id, text):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)


def booking_form(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Проверь, есть ли документы
            privacy_policy = PrivacyPolicy.objects.first()
            consent_form = ConsentForm.objects.first()
            
            if not privacy_policy or not consent_form:
                return JsonResponse({'success': False, 'error': 'Документы политики и согласия не найдены'})

            booking.privacy_policy = privacy_policy
            booking.consent_form = consent_form
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
