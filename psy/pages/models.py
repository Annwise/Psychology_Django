from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(verbose_name='Содержание')

    class Meta:
        verbose_name = 'Политика конфиденциальности'
        verbose_name_plural = 'Политика конфиденциальности'

    def __str__(self):
        return self.title


class ConsentForm(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(verbose_name='Содержание')

    class Meta:
        verbose_name = 'Форма согласия'
        verbose_name_plural = 'Формы согласия'

    def __str__(self):
        return self.title


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждена'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    privacy_policy = models.ForeignKey(PrivacyPolicy, on_delete=models.CASCADE, verbose_name='Политика конфиденциальности', null=True, blank=True)
    consent_form = models.ForeignKey(ConsentForm, on_delete=models.CASCADE, verbose_name='Форма согласия', null=True, blank=True)
    accepted_privacy_policy = models.BooleanField(default=False, verbose_name='Согласие на политику конфиденциальности')
    accepted_consent = models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(blank=True, verbose_name='Сообщение')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.phone}'


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, verbose_name='Пол')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.user.username} - Профиль'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


class BookingStatus(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждена'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, verbose_name='Запись')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Статус записи'
        verbose_name_plural = 'Статусы записей'

    def __str__(self):
        return f'{self.booking.name} - {self.get_status_display()}'
