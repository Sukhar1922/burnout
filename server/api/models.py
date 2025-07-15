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
        return f'{self.People_ID} от {self.Date_Record}'


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
