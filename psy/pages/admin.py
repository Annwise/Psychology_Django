from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Booking, UserProfile, PrivacyPolicy, ConsentForm, BookingStatus


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_editable = ['status']
    date_hierarchy = 'created_at'  # Можно оставить, если есть поле created_at


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль пользователя'


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'gender', 'birth_date']
    list_filter = ['gender']
    search_fields = ['user__username', 'user__email']


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(ConsentForm)
class ConsentFormAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(BookingStatus)
class BookingStatusAdmin(admin.ModelAdmin):
    list_display = ['booking', 'get_status_display', 'updated_at']
    list_filter = ['status', 'updated_at']
    search_fields = ['booking__name', 'booking__email']
