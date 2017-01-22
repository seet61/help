from django.db import models

# Create your models here.

class Tasks(models.Model):
	number = models.CharField(max_length=10)
	login = models.CharField(max_length=32)
	activity_date = models.DateField()
	comment = models.CharField(max_length=2048)

class Over_Time(models.Model):
	login = models.CharField(max_length=32)
	activity_date = models.DateField()
	comment = models.CharField(max_length=2048)