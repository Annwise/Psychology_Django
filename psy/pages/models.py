from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Описание')
    price = models.CharField(max_length=100, verbose_name='Цена')
    duration = models.CharField(max_length=100, verbose_name='Продолжительность', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['title']

    def __str__(self):
        return self.title


class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(verbose_name='Содержание')
    version = models.CharField(max_length=50, verbose_name='Версия')
    effective_date = models.DateTimeField(verbose_name='Дата вступления в силу')

    class Meta:
        verbose_name = 'Политика конфиденциальности'
        verbose_name_plural = 'Политики конфиденциальности'

    def __str__(self):
        return self.title


class ConsentForm(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(verbose_name='Содержание')
    version = models.CharField(max_length=50, verbose_name='Версия')
    effective_date = models.DateTimeField(verbose_name='Дата вступления в силу')

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
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
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


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.CharField(max_length=100, verbose_name='Автор')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_date']

    def __str__(self):
        return self.title


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('certificate', 'Сертификат'),
        ('diploma', 'Диплом'),
        ('license', 'Лицензия'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name='Тип документа')
    file = models.FileField(upload_to='documents/', verbose_name='Файл')
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['-upload_date']

    def __str__(self):
        return self.title


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
