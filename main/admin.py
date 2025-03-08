from django.utils import timezone  # Импортируем timezone

from django.contrib import admin


# Register your models here.
from main.models import Main, AboutUs, Team, Blog, ContactUs


@admin.register(Main)
class MainAdmin(admin.ModelAdmin):
    list_display = ('site_name',)


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("photo", "description", "year_in_business", "happy_people", "sales", "award_winning")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo', 'job_title', 'instagram', 'facebook')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('email',)


