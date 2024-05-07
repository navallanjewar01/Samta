from django.contrib import admin
from .models import CustomUser, Tenant

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tenant)