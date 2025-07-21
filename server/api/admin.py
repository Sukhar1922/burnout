from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.urls import path
from django.shortcuts import redirect
from .models import *

from django.core.cache import cache

from .BurnoutLib.BurnoutLib import HandlerQuestions, getFakeStatistics

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
    # fields = (
    #     'Voltage_symptomSum',
    #     'resistance_symptomSum',
    #     'exhaustion_symptomSum',
    #     'Summary_Value',
    # )
    actions = None

    def has_change_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        instance = self.get_object(request, object_id)

        statistics = getFakeStatistics([
            instance.Voltage_symptom1,
            instance.Voltage_symptom2,
            instance.Voltage_symptom3,
            instance.Voltage_symptom4,
            instance.resistance_symptom1,
            instance.resistance_symptom2,
            instance.resistance_symptom3,
            instance.resistance_symptom4,
            instance.exhaustion_symptom1,
            instance.exhaustion_symptom2,
            instance.exhaustion_symptom3,
            instance.exhaustion_symptom4,
        ])

        PHASE_NAMES = [
            [
                'НАПРЯЖЕНИЕ',
                [
                    'Переживание психотравмирующих обстоятельств',
                    'Неудовлетворенность собой',
                    '\"Загнанность в клетку\"',
                    'Тревога и депрессия',
                ],
                '''Характеризуется ощущением эмоционального истощения,
                усталости, вызванной собственной профессиональной деятельностью.'''
            ],
            [
                'РЕЗИСТЕНЦИЯ',
                [
                    'Неадекватное избирательное эмоциональное реагирование',
                    'Эмоционально-нравственная дезориентация',
                    'Расширение сферы экономии эмоций',
                    'Редукция профессиональных обязанностей',
                ],
                '''Характеризуется избыточным эмоциональным
                истощением, которое провоцирует развитие и возникновения защитных
                реакций, которые делают человека эмоционально закрытым, отстраненным,
                безразличным. На таком фоне любое эмоциональное привлечение к
                профессиональной деятельности и коммуникации вызывает у человека
                чувство избыточного переутомления.'''
            ],
            [
                'ИСТОЩЕНИЕ',
                [
                    'Эмоциональный дефицит',
                    'Эмоциональная отстраненность',
                    'Личностная отстраненность (деперсонализация)',
                    'Психосоматические и психовегетативные нарушения',
                ],
                '''Характеризуется психофизическим переутомлением
                человека, опустошенностью, нивелированием собственных
                профессиональных достижений, нарушением профессиональных
                коммуникаций, развитием циничного отношения к тем, с кем приходится
                общаться, развитием психосоматических нарушений.'''
            ],
        ]

        extra_context['phases'] = [
            {
                'name': PHASE_NAMES[i][0],
                'status': statistics[i][1],
                'points': statistics[i][0],
                'help': PHASE_NAMES[i][2],
                'symptoms': [
                    {
                        'name': PHASE_NAMES[i][1][j],
                        'status': statistics[i][2][j][1],
                        'points': statistics[i][2][j][0]
                    } for j in range(len(PHASE_NAMES[i][1]))
                ]
            } for i in range(len(PHASE_NAMES))
            # {
            #     'name': 'НАПРЯЖЕНИЕ',
            #     'status': 'высокий',
            #     'points': 47,
            #     'symptoms': [
            #         {'name': 'Симптом 1', 'status': 'высокий', 'points': 12},
            #         {'name': 'Симптом 2', 'status': 'высокий', 'points': 10},
            #         # ...
            #     ]
            # },
            # # ...
        ]

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )