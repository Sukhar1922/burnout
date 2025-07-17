from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.urls import path
from django.shortcuts import redirect
from .models import *

from django.core.cache import cache

# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.delete('questions_cache')  # Сброс кэша

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        cache.delete('questions_cache')  # Сброс кэша

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('clear-cache/', self.admin_site.admin_view(self.clear_cache), name='clear_questions_cache'),
        ]
        return custom_urls + urls

    def clear_cache(self, request):
        cache.delete('questions_cache')
        self.message_user(request, "Кэш вопросов сброшен.")
        return redirect('..')

    change_list_template = "admin/questions_change_list.html"


class TestBurnoutInline(admin.TabularInline):
    model = Test_Burnout
    extra = 0
    readonly_fields = ('Date_Record', 'Voltage_symptomSum', 'resistance_symptomSum', 'exhaustion_symptomSum', 'Summary_Value')
    fields = (
        'Date_Record',
        'Voltage_symptomSum',
        'resistance_symptomSum',
        'exhaustion_symptomSum',
        'Summary_Value',
    )
    can_delete = False
    list_filter = ('Date_Record',)
    ordering = ('-Date_Record',)
    show_change_link = True


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    # list_display = ('Surname', 'Name', 'Email', 'TG_ID')
    search_fields = ('Surname', 'Name', 'Patronymic')
    search_help_text = 'Для поиска введите что-то из следующего: Фамилия, Имя, Отчество пользователя'
    inlines = [TestBurnoutInline]
    actions = None

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Test_Burnout)
class TestBurnoutAdmin(admin.ModelAdmin):
    list_display = ('People_ID', 'Date_Record', 'Summary_Value')
    list_filter = ('Date_Record', 'People_ID')
    search_fields = ('People_ID__Surname', 'People_ID__Name', 'People_ID__Patronymic')
    search_help_text = 'Для поиска введите что-то из следующего: Фамилия, Имя, Отчество пользователя'
    actions = None

    def has_change_permission(self, request, obj=None):
        return False