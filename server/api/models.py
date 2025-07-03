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

    def __str__(self):
        return f'{self.Surname} {self.Name}'


class Phase_VOLTAGE(models.Model):
    id = models.AutoField(primary_key=True)
    People_ID = models.ForeignKey(to=People, on_delete=models.CASCADE, related_name='VOLTAGE')
    Date_Record = models.DateTimeField(auto_now_add=True)
    Symptom1 = models.IntegerField(null=True)
    Symptom2 = models.IntegerField(null=True)
    Symptom3 = models.IntegerField(null=True)
    Symptom4 = models.IntegerField(null=True)
    SymptomSum = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.People_ID.TG_ID} от {self.Date_Record}'


class Phase_RESISTANCE(models.Model):
    id = models.AutoField(primary_key=True)
    People_ID = models.ForeignKey(to=People, on_delete=models.CASCADE, related_name='RESISTANCE')
    Date_Record = models.DateTimeField(auto_now_add=True)
    Symptom1 = models.IntegerField(null=True)
    Symptom2 = models.IntegerField(null=True)
    Symptom3 = models.IntegerField(null=True)
    Symptom4 = models.IntegerField(null=True)
    SymptomSum = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.People_ID.TG_ID} от {self.Date_Record}'


class Phase_EXHAUSTION(models.Model):
    id = models.AutoField(primary_key=True)
    People_ID = models.ForeignKey(to=People, on_delete=models.CASCADE, related_name='EXHAUSTION')
    Date_Record = models.DateTimeField(auto_now_add=True)
    Symptom1 = models.IntegerField(null=True)
    Symptom2 = models.IntegerField(null=True)
    Symptom3 = models.IntegerField(null=True)
    Symptom4 = models.IntegerField(null=True)
    SymptomSum = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.People_ID.TG_ID} от {self.Date_Record}'


class Test_Burnout(models.Model):
    id = models.AutoField(primary_key=True)
    People_ID = models.ForeignKey(to=People, on_delete=models.CASCADE, related_name='Burnout')
    Date_Record = models.DateTimeField(auto_now_add=True)
    VOLTAGE = models.ForeignKey(to=Phase_VOLTAGE, on_delete=models.CASCADE, related_name='Burnout')
    RESISTANCE = models.ForeignKey(to=Phase_RESISTANCE, on_delete=models.CASCADE, related_name='Burnout')
    EXHAUSTION = models.ForeignKey(to=Phase_EXHAUSTION, on_delete=models.CASCADE, related_name='Burnout')
    Summary_Value = models.IntegerField()

    def __str__(self):
        return f'{self.People_ID.TG_ID} от {self.Date_Record}'


class Questions(models.Model):
    id = models.AutoField(primary_key=True)
    Name_Question = models.TextField(null=False, blank=False)
    Points_Answer_Yes = models.IntegerField(null=False, blank=False)
    Points_Answer_No = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.Name_Question}'
