from django.contrib import admin
from .models import Service, Booking

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'duration', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    prepopulated_fields = {'title': ('title',)}

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'service', 'date', 'status', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_editable = ['status']
    date_hierarchy = 'date'
