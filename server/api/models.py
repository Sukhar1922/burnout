import datetime

from django.db import models

# Create your models here.
class People(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=32, null=False, verbose_name=u"Имя")
    Surname = models.CharField(max_length=32, null=False, verbose_name=u"Фамилия")
    Patronymic = models.CharField(max_length=32, null=True, verbose_name=u"Отчество")
    Email = models.CharField(max_length=64, null=False, verbose_name=u"Эл. почта")
    Birthday = models.DateField(null=True, blank=True, verbose_name=u"День рождения")
    TG_ID = models.CharField(max_length=64, null=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.Surname} {self.Name}'


class Test_Burnout(models.Model):
    id = models.AutoField(primary_key=True)
    People_ID = models.ForeignKey(to=People, on_delete=models.CASCADE, related_name='Burnout', verbose_name=u"Пользователь")
    Date_Record = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата выполнения")
    Voltage_symptom1 = models.IntegerField(verbose_name=u"Переж. обст.")
    Voltage_symptom2 = models.IntegerField(verbose_name=u"Неуд. собой")
    Voltage_symptom3 = models.IntegerField(verbose_name=u"Загнанность")
    Voltage_symptom4 = models.IntegerField(verbose_name=u"Тревога")
    Voltage_symptomSum = models.IntegerField(verbose_name=u"Сумма напряжения")
    resistance_symptom1 = models.IntegerField(verbose_name=u"Эм. реакция")
    resistance_symptom2 = models.IntegerField(verbose_name=u"Эм. дезор.")
    resistance_symptom3 = models.IntegerField(verbose_name=u"Расш. сферы")
    resistance_symptom4 = models.IntegerField(verbose_name=u"Редукция")
    resistance_symptomSum = models.IntegerField(verbose_name=u"Сумма резистенции")
    exhaustion_symptom1 = models.IntegerField(verbose_name=u"Эм. дефицит")
    exhaustion_symptom2 = models.IntegerField(verbose_name=u"Эм. отстр.")
    exhaustion_symptom3 = models.IntegerField(verbose_name=u"Лич. отстр.")
    exhaustion_symptom4 = models.IntegerField(verbose_name=u"Психосоматика")
    exhaustion_symptomSum = models.IntegerField(verbose_name=u"Сумма истощения")
    Summary_Value = models.IntegerField(verbose_name=u"Сумма баллов")

    class Meta:
        verbose_name = 'Пройденный тест'
        verbose_name_plural = 'Пройденные тесты'

    def __str__(self):
        return f'Тест {self.People_ID} от {self.Date_Record.date()}'


class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    Name_Question = models.TextField(null=False, blank=False, verbose_name=u"Вопрос")
    Points_Answer_Yes = models.IntegerField(null=False, blank=False, verbose_name=u"Баллов за \"Да\"")
    Points_Answer_No = models.IntegerField(null=False, blank=False, verbose_name=u"Баллов за \"Нет\"")

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.Name_Question}'


class Everyweek_Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    Phase = models.TextField(null=False, blank=False, verbose_name=u"Фаза задания")
    Name = models.TextField(null=False, blank=False, verbose_name=u"Название задания")
    Text = models.TextField(null=False, blank=False, verbose_name=u"Текст задания")

    class Meta:
        verbose_name = 'Тип еженедельного задания'
        verbose_name_plural = 'Типы еженедельного задания'

    def __str__(self):
        return f'Тип задания {self.Phase}: {self.Name}'


class Answers_Everyweek_Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    TestID = models.ForeignKey(to=Test_Burnout, on_delete=models.CASCADE, related_name='Answers_everyweek_task',
                               verbose_name=u"Тест выгорания")
    TaskID = models.ForeignKey(to=Everyweek_Tasks, on_delete=models.PROTECT, related_name='Answers_everyweek_task',
                               verbose_name=u"Тип еженедельного задания")
    Date_Record = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата взятия задания")
    Stars = models.IntegerField(null=True, blank=True, verbose_name=u"Количество звёзд")
    Comments = models.TextField(null=True, blank=True, verbose_name=u"Комментарий к заданию")
    NotificationSent = models.BooleanField(default=False, verbose_name=u"Уведомление было отправлено?")

    class Meta:
        verbose_name = 'Еженедельное задание'
        verbose_name_plural = 'Еженедельные задания'

    def __str__(self):
        return f'Еженедельное задание {self.TestID}, {self.TaskID.Name}'


class Options(models.Model):
    People_ID = models.OneToOneField(to=People, on_delete=models.CASCADE, related_name='options',
                                  verbose_name=u"Пользователь", primary_key=True)
    Notification_Day = models.BooleanField(default=True)
    Notification_Day_Time = models.TimeField(null=True, blank=True, default=datetime.time(20, 30),
                                             verbose_name="Уведомления на ежедневные задания")
    Notification_Week = models.BooleanField(default=True)
    Notification_Week_Time = models.TimeField(null=True, blank=True, default=datetime.time(19, 0),
                                             verbose_name="Уведомления на еженедельные задания")

    class Meta:
        verbose_name = 'Настройки пользователя'
        verbose_name_plural = 'Настройки пользователя'

    def __str__(self):
        return f'Настройки {self.People_ID}'

