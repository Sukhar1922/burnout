from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from .models import *

from django.core.cache import cache

# Register your models here.
# admin.site.register(Questions)
admin.site.register(People)
admin.site.register(Phase_VOLTAGE)
admin.site.register(Phase_RESISTANCE)
admin.site.register(Phase_EXHAUSTION)
admin.site.register(Test_Burnout)

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