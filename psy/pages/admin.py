from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Service, Booking, Article, Document, UserProfile, PrivacyPolicy, ConsentForm


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'duration', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    prepopulated_fields = {'title': ('title',)}


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_editable = ['status']
    date_hierarchy = 'created_at'  # Можно оставить, если есть поле created_at


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_active', 'published_date']
    list_filter = ['is_active', 'published_date', 'author']
    search_fields = ['title', 'content', 'author']
    list_editable = ['is_active']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'upload_date']
    list_filter = ['document_type', 'upload_date']
    search_fields = ['title', 'document_type']


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
    search_fields = ['user__username', 'user__first_name', 'phone']


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['title', 'version', 'effective_date']
    list_filter = ['effective_date']


@admin.register(ConsentForm)
class ConsentFormAdmin(admin.ModelAdmin):
    list_display = ['title', 'version', 'effective_date']
    list_filter = ['effective_date']
