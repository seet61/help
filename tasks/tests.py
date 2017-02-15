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

#tests
class TasksPostActivityTestCase(TestCase):
    def test_add_activity(self):
        for rec in xrange(1,11):
            integer = random.randrange(1000000, 1500000) 
            number = random.choice(index) + str(integer)
            calendar = date(random.choice(year_range), random.choice(month_range), random.choice(day_range)).strftime('%d %B, %Y')
            calendar = datetime.strptime(calendar, '%d %B, %Y').date()
            Tasks.objects.create(number=number, login=user, activity_date=calendar, comment='test comment for %s' % number).save()
        print 'Count of added redords for activities: %s'  % rec

    def test_list_activity(self):
        for rec in xrange(0,11):
            calendar_start = date(random.choice(year_range), random.choice(month_range), random.choice(day_range)).strftime('%d %B, %Y')
            calendar_start = datetime.strptime(calendar_start, '%d %B, %Y').date()
            calendar_end = date(random.choice(year_range), random.choice(month_range), random.choice(day_range)).strftime('%d %B, %Y')
            calendar_end = datetime.strptime(calendar_end, '%d %B, %Y').date()
            entries = Tasks.objects.filter(login=user).filter(activity_date__range=(calendar_start, calendar_end))
            if calendar_start > calendar_end:
                self.assertEqual(len(entries), 0)
            else:
                self.assertEqual(len(entries), len(entries))

class TasksPostOvertimeTestCase(TestCase):
    def test_add_overtime(self):
        for rec in xrange(1,11):
            calendar = date(random.choice(year_range), random.choice(month_range), random.choice(day_range)).strftime('%d %B, %Y')
            calendar = datetime.strptime(calendar, '%d %B, %Y').date()
            Over_Time(login=user, activity_date=calendar, comment='test comment for %s' % calendar).save()
        print 'Count of added redords for overtimes: %s'  % rec

    def test_list_overtime(self):
        for rec in xrange(0,11):
            calendar_start = date(random.choice(year_range), random.choice(month_range), random.choice(day_range)).strftime('%d %B, %Y')
            calendar_start = datetime.strptime(calendar_start, '%d %B, %Y').date()
            calendar_end = date(random.choice(year_range), random.choice(month_range), random.choice(day_range)).strftime('%d %B, %Y')
            calendar_end = datetime.strptime(calendar_end, '%d %B, %Y').date()
            entries = Over_Time.objects.filter(login=user).filter(activity_date__range=(calendar_start, calendar_end))
            if calendar_start > calendar_end:
                self.assertEqual(len(entries), 0)
            else:
                self.assertEqual(len(entries), len(entries))

class TasksUITestCase(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_get_index_page(self):
        response = self.client.get('/tasks/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
