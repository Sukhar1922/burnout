from django.db import models

# Create your models here.
class People(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=32, null=False)
    Surname = models.CharField(max_length=32, null=False)
    Patronymic = models.CharField(max_length=32, null=True)
    Email = models.CharField(max_length=64, null=False)
    Birthday = models.DateField(null=True, blank=True)
    TG_ID = models.CharField(max_length=64, null=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.Surname} {self.Name}'


class Test_Burnout(models.Model):
    id = models.AutoField(primary_key=True)
    People_ID = models.ForeignKey(to=People, on_delete=models.CASCADE, related_name='Burnout')
    Date_Record = models.DateTimeField(auto_now_add=True)
    Voltage_symptom1 = models.IntegerField()
    Voltage_symptom2 = models.IntegerField()
    Voltage_symptom3 = models.IntegerField()
    Voltage_symptom4 = models.IntegerField()
    Voltage_symptomSum = models.IntegerField()
    resistance_symptom1 = models.IntegerField()
    resistance_symptom2 = models.IntegerField()
    resistance_symptom3 = models.IntegerField()
    resistance_symptom4 = models.IntegerField()
    resistance_symptomSum = models.IntegerField()
    exhaustion_symptom1 = models.IntegerField()
    exhaustion_symptom2 = models.IntegerField()
    exhaustion_symptom3 = models.IntegerField()
    exhaustion_symptom4 = models.IntegerField()
    exhaustion_symptomSum = models.IntegerField()
    Summary_Value = models.IntegerField()

    class Meta:
        verbose_name = 'Пройденный тест'
        verbose_name_plural = 'Пройденные тесты'

    def __str__(self):
        return f'{self.People_ID.TG_ID} от {self.Date_Record}'


class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    Name_Question = models.TextField(null=False, blank=False)
    Points_Answer_Yes = models.IntegerField(null=False, blank=False)
    Points_Answer_No = models.IntegerField(null=False, blank=False)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.Name_Question}'
