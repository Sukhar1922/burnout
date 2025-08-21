from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.urls import path
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import redirect
from .models import *

from django.core.cache import cache

from .BurnoutLib.BurnoutLib import HandlerQuestions, getFakeStatistics

# Register your models here.

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Answers_Everyweek_Tasks)

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

    readonly_fields = (
        'id',
        'Name_Question',
        'Points_Answer_Yes',
        'Points_Answer_No',
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


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


class AnswersEveryweekTasksInline(admin.TabularInline):
    model = Answers_Everyweek_Tasks
    extra = 0
    readonly_fields = (
        'Date_Record',
        'task_phase',
        'task_name',
        'stars_count',
        'numbering'
    )
    fields = (
        'numbering',
        'task_phase',
        'task_name',
        'Date_Record',
        'stars_count',
    )
    can_delete = False
    list_filter = ('Date_Record',)
    ordering = ('-Date_Record',)
    show_change_link = True

    def task_phase(self, obj):
        return obj.TaskID.Phase

    task_phase.short_description = "Фаза задания"

    def task_name(self, obj):
        return obj.TaskID.Name

    task_name.short_description = "Название задания"

    def stars_count(self, obj):
        if obj.Stars:
            return obj.Stars
        return 'не выполнено/не оценено'

    stars_count.short_description = "Оценка"

    def numbering(self, obj):
        qs = list(
            Answers_Everyweek_Tasks.objects.filter(TestID=obj.TestID).order_by('Date_Record')
        )
        return qs.index(obj) + 1

    numbering.short_description = "Неделя"

@admin.register(Test_Burnout)
class TestBurnoutAdmin(admin.ModelAdmin):
    list_display = ('People_ID', 'Date_Record', 'Summary_Value')
    list_filter = ('Date_Record', 'People_ID')
    search_fields = ('People_ID__Surname', 'People_ID__Name', 'People_ID__Patronymic')
    search_help_text = 'Для поиска введите что-то из следующего: Фамилия, Имя, Отчество пользователя'
    inlines = [AnswersEveryweekTasksInline]
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
                    [
                        'Переживание психотравмирующих обстоятельств',
                        '''Человек воспринимает
                        условия работы и профессиональные межличностные отношения как
                        психотравмирующие'''
                    ],
                    [
                        'Неудовлетворенность собой',
                        '''Недовольство собственной профессиональной
                        деятельностью и собой как профессионалом'''
                    ],
                    [
                        '\"Загнанность в клетку\"',
                        '''Ощущение безвыходности ситуации, желание
                        изменить работу или вообще профессиональную деятельность'''
                    ],
                    [
                        'Тревога и депрессия',
                        '''Развитие тревожности в профессиональной
                        деятельности, повышение нервности, депрессивные настроения'''
                    ],
                ],
                '''Характеризуется ощущением эмоционального истощения,
                усталости, вызванной собственной профессиональной деятельностью.'''
            ],
            [
                'РЕЗИСТЕНЦИЯ',
                [
                    [
                        'Неадекватное избирательное эмоциональное реагирование',
                        '''Не контролированное влияние настроения на профессиональные отношения'''
                    ],
                    [
                        'Эмоционально-нравственная дезориентация',
                        '''Развитие безразличия в профессиональных отношениях'''
                    ],
                    [
                        'Расширение сферы экономии эмоций',
                        '''Эмоциональная замкнутость, отчуждение, желание прекратить любые коммуникации'''
                    ],
                    [
                        'Редукция профессиональных обязанностей',
                        '''Свертывание профессиональной деятельности, стремление как можно меньше времени
                        тратить на выполнение профессиональных обязанностей'''
                    ],
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
                    [
                        'Эмоциональный дефицит',
                        '''Развитие эмоциональной бесчувственности на
                        фоне переутомления, минимизация эмоционального вклада в работу,
                        автоматизм и опустошение человека при выполнении профессиональных
                        обязанностей'''
                    ],
                    [
                        'Эмоциональная отстраненность',
                        '''Создание защитного барьера в профессиональных коммуникациях'''
                    ],
                    [
                        'Личностная отстраненность (деперсонализация)',
                        '''Нарушение профессиональных отношений, развитие циничного отношения к тем, с кем
                        приходится общаться'''
                    ],
                    [
                        'Психосоматические и психовегетативные нарушения',
                        '''Ухудшение физического самочувствия,
                        развитие таких психосоматических нарушений, как расстройства сна,
                        головная боль, проблемы с давлением'''
                    ],
                ],
                '''Характеризуется психофизическим переутомлением
                человека, опустошенностью, нивелированием собственных
                профессиональных достижений, нарушением профессиональных
                коммуникаций, развитием циничного отношения к тем, с кем приходится
                общаться, развитием психосоматических нарушений.'''
            ],
        ]
        user_obj = instance.People_ID
        user_url = reverse('admin:api_people_change', args=[user_obj.pk])
        user_link = format_html('<a href="{}">{}</a>', user_url, user_obj)
        extra_context['people'] = user_link
        extra_context['phases'] = [
            {
                'name': PHASE_NAMES[i][0],
                'status': statistics[i][1],
                'points': statistics[i][0],
                'help': PHASE_NAMES[i][2],
                'symptoms': [
                    {
                        'name': PHASE_NAMES[i][1][j][0],
                        'status': statistics[i][2][j][1],
                        'points': statistics[i][2][j][0],
                        'help': PHASE_NAMES[i][1][j][1],
                    } for j in range(len(PHASE_NAMES[i][1]))
                ]
            } for i in range(len(PHASE_NAMES))
        ]

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )


@admin.register(Everyweek_Tasks)
class EveryweekTasksAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id',
        'Phase',
        'Name',
        'Text',
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
