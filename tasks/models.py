from django.db import models
import datetime

# Create your models here.

class Tasks(models.Model):
	number = models.CharField(max_length=10)
	login = models.CharField(max_length=32)
	activity_date = models.DateField(db_index=True)
	comment = models.CharField(max_length=2048)

class Over_Time(models.Model):
	login = models.CharField(max_length=32)
	activity_date = models.DateField(db_index=True)
	comment = models.CharField(max_length=2048)

class Works(models.Model):
	number = models.CharField(max_length=10)
	login = models.CharField(max_length=32)
	activity_date = models.DateField(db_index=True)
	field = models.BooleanField(default=False)
	installed = models.CharField(max_length=4096)
	restarted = models.CharField(max_length=4096)
	passwords_users = models.CharField(max_length=4096, default='')
	logs = models.CharField(max_length=1024)
	problems = models.CharField(max_length=4096, default='')
	call_CC = models.BooleanField(default=False)
	time_CC = models.TimeField(default=datetime.time(0))
	whatsapp = models.BooleanField(default=False)
	sms = models.BooleanField(default=False)
	comment = models.CharField(max_length=2048)

class ToDo(models.Model):
	target = models.CharField(max_length=2048)
	reason = models.CharField(max_length= 32)
	#duedate = models.DateField(db_index=True)
	finished = models.BooleanField(db_index=True)
		