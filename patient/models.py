from django.db import models

# Create your models here.

class DiabetesData(models.Model):
    Pregnancies=models.IntegerField()
    Glucose=models.IntegerField()
    BloodPressure=models.IntegerField()
    SkinThickness=models.IntegerField()
    Insulin=models.IntegerField()
    BMI=models.FloatField()
    DiabetesPedigreeFunction=models.FloatField()
    Age=models.IntegerField()




class WebsiteUser(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.EmailField(max_length=67)
    password=models.CharField(max_length=67)
    username=models.CharField(max_length=89)




