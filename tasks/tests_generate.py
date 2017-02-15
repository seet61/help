# Create your tests here.
from django.test import TestCase
from django.test import Client

from tasks.models import *
import random
from datetime import datetime, date

index = ['IM', 'C', 'Q']
year_range = [2016, 2017]
month_range = [i for i in range(1, 12)]
day_range = [i for i in range(1,28)]
user = 'darefyev'

#generate entries
class GeneratePostActivityTestCase(TestCase):
    for rec in xrange(1,11):
        integer = random.randrange(1000000, 1500000) 
        number = random.choice(index) + str(integer)
        calendar = date(random.choice(year_range), random.choice(month_range), random.choice(day_range)).strftime('%d %B, %Y')
        calendar = datetime.strptime(calendar, '%d %B, %Y').date()
        Tasks.objects.create(number=number, login=user, activity_date=calendar, comment='test comment for %s' % number).save()
    print 'Count of added redords: %s'  % rec


class GeneratePostOvertimeTestCase(TestCase):
    for rec in xrange(1,11):
        calendar = date(random.choice(year_range), random.choice(month_range), random.choice(day_range)).strftime('%d %B, %Y')
        calendar = datetime.strptime(calendar, '%d %B, %Y').date()
        Over_Time(login=user, activity_date=calendar, comment='test comment for %s' % calendar).save()
    print 'Count of added redords for overtimes: %s'  % rec