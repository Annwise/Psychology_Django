from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import Booking, PrivacyPolicy, ConsentForm, BookingStatus
from .forms import BookingForm, CustomUserRegisterForm, CustomAuthenticationForm
import telegram
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
import logging
import threading
import csv
from datetime import datetime
import os

logger = logging.getLogger('pages')


def home(request):
    form = BookingForm()
    return render(request, 'pages/home.html', {
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
            logger.info(f'Пользователь {user.username} вошёл')
            return redirect('home')
        else:
            error_text = ' '.join([str(error) for error in form.errors.values()])
            logger.warning(f'Ошибка входа: {error_text}')
            return render(request, 'pages/login.html', {'form': form})
    else:
        form = CustomAuthenticationForm()

    return render(request, 'pages/login.html', {'form': form})


async def send_telegram_message(chat_id, text):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)


def generate_booking_report_async(booking):
    # Функция, которая создаёт отчёт в фоне
    report_dir = os.path.join(settings.BASE_DIR, 'reports')
    os.makedirs(report_dir, exist_ok=True)

    report_path = os.path.join(report_dir, f'booking_report_{booking.id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

    with open(report_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'email', 'phone', 'created_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({
            'id': booking.id,
            'name': booking.name,
            'email': booking.email,
            'phone': booking.phone,
            'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    logger.info(f'Отчёт по записи {booking.id} создан: {report_path}')


def booking_form(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Проверь, есть ли документы
            privacy_policy = PrivacyPolicy.objects.first()
            consent_form = ConsentForm.objects.first()

            if not privacy_policy or not consent_form:
                logger.error('Документы политики и согласия не найдены')
                return JsonResponse({'success': False, 'error': 'Документы политики и согласия не найдены'})

            booking.privacy_policy = privacy_policy
            booking.consent_form = consent_form
            booking.accepted_privacy_policy = True
            booking.accepted_consent = True

            booking.save()

            logger.info(f'Новая запись: {booking.name} ({booking.email})')

            # Создаём статус для записи
            BookingStatus.objects.create(booking=booking, status='pending')

            # Создаём отчёт в фоне
            thread = threading.Thread(target=generate_booking_report_async, args=(booking,))
            thread.start()

            # Отправка уведомления в Telegram
            try:
                import asyncio
                asyncio.run(send_telegram_message('705925519', f'Новая запись: {booking.name}, {booking.phone}, {booking.email}'))
            except Exception as e:
                logger.error(f'Ошибка отправки в Telegram: {e}')
                print(f'Ошибка отправки в Telegram: {e}')

            return JsonResponse({'success': True})
        else:
            logger.warning(f'Ошибка валидации формы: {form.errors}')
            return JsonResponse({'success': False, 'error': 'Пожалуйста, заполните все поля корректно'})

    return JsonResponse({'success': False, 'error': 'Метод не разрешён'})


def privacy_policy(request):
    policy = PrivacyPolicy.objects.last()
    return render(request, 'pages/privacy.html', {'policy': policy})


def consent_form(request):
    consent = ConsentForm.objects.last()
    return render(request, 'pages/consent.html', {'consent': consent})


def is_admin(user):
    return user.is_staff


@login_required
def user_profile(request):
    # Личный кабинет — показывает только записи текущего пользователя
    bookings = Booking.objects.filter(email=request.user.email)
    return render(request, 'pages/profile.html', {'bookings': bookings})


@login_required
@user_passes_test(is_admin)
def admin_bookings(request):
    # Страница для админа
    bookings = Booking.objects.all()
    return render(request, 'pages/admin_bookings.html', {'bookings': bookings})


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)
