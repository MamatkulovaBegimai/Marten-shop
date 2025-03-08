from django.contrib import admin

# Register your models here.

# Register your models here.
from user.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username',)