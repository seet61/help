from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts  import redirect
from datetime import datetime, date
from django.contrib.auth.models import User
#from django.core.exceptions import DoesNotExist

from .models import Tasks, Over_Time
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
	#method for index page
	if request.user.is_authenticated():
		return render(request, 'tasks/index.html')
	else:
		return render(request, 'tasks/login.html')

def settings(request):
	#method for settings page
	if request.user.is_authenticated():
		return render(request, 'tasks/settings.html')
	else:
		return render(request, 'tasks/login.html')

def change_password(request):
	#method for changing password from settings page
	if request.user.is_authenticated():
		if request.method == 'POST':
			user = request.user
			try:
				current_password = request.POST['current_password']
				new_password = request.POST['new_password']
				confirm_password = request.POST['confirm_password']
				print current_password, new_password, confirm_password
				if (new_password == confirm_password):
					print new_password == confirm_password
					#user = authenticate(username=user, password=current_password)
					#print user
					if ((authenticate(username=user, password=current_password)) is not None):
						u = User.objects.get(username=user)
						u.set_password(new_password)
						u.save()
						return render(request, 'tasks/settings.html', {'password_changed' : 1})
					else:
						return render(request, 'tasks/settings.html', {'bad_data' : 1})
				else:
					return render(request, 'tasks/settings.html', {'bad_confirm' : 1})
			except Exception as e:
				#logging.DEBUG(e)
				return render(request, 'tasks/settings.html', {'bad_data' : 1})
		else:
			return render(request, 'tasks/settings.html')
	else:
		return render(request, 'tasks/login.html')


def login(request):
	#login method
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if (user is not None) == True:
			print 'Active: ', user.is_active
			if user.is_active:
				auth_login(request, user)
				logging.info('User %s is autorized' % user)
				return render(request, 'tasks/index.html')
			else:
				logging.warning('User %s is blocked' % user)
				return render(request, 'tasks/login.html', {'disabled_acc' : 1})
		else:
			return render(request, 'tasks/login.html', {'invalid_data' : 1})


	else:
		return render(request, 'tasks/login.html')

def logout_view(request):
	#logout method
	if request.user.is_authenticated():
		logout(request)
		return render(request, 'tasks/login.html')
	else:
		logger.error('User try logout when not logged')
		return render(request, 'tasks/login.html')

def post_task(request):
	#method for add new task
	if request.user.is_authenticated():
		if request.method == 'POST':
			user = request.user
			try:
				number = request.POST['number']
				calendar = request.POST['calendar']
				calendar = datetime.strptime(calendar, '%d %B, %Y').date()
				comment = request.POST['comment']
				if (number is not None) and (calendar is not None) and (comment is not None) :
					try:
						entry = Tasks.objects.filter(number=number).filter(login=user)
						print 'len ', len(entry)
						if len(entry) != 0:
							return render(request, 'tasks/post_task.html', {'task_saved' : 2})
						else:
							insert = Tasks(number=number, login=user, activity_date=calendar, comment=comment)
							insert.save()
							return render(request, 'tasks/post_task.html', {'task_saved' : 1})
					except Exception as e:
						print 'Exception ', e
						return render(request, 'tasks/post_task.html', {'task_saved' : 0})
				else:
					return render(request, 'tasks/post_task.html')
			except Exception as e:
				print 'Exception ', e
				return render(request, 'tasks/post_task.html', {'task_saved' : 0})
		else:
			number = None
			calendar = None
			comment = None
			return render(request, 'tasks/post_task.html')
	else:
		return render(request, 'tasks/login.html')


def list_tasks(request):
	#method for list tasks between days
	if request.user.is_authenticated():
		if request.method == 'POST':
			user = request.user
			entries = {}
			try:
				calendar_start = request.POST['calendar_start']
				calendar_start = datetime.strptime(calendar_start, '%d %B, %Y').date()
				calendar_end = request.POST['calendar_end']
				calendar_end = datetime.strptime(calendar_end, '%d %B, %Y').date()
				#print user, calendar_start, calendar_end
				entries = Tasks.objects.filter(login=user).filter(activity_date__range=(calendar_start, calendar_end))
				changes = []
				queries = []
				others = []
				for entry in entries:
					if entry.number[0] == 'C':
						changes.append(entry)
					elif entry.number[0] == 'Q':
						queries.append(entry)
					else:
						others.append(entry)
				return render(request, 'tasks/list_tasks.html', {'changes': changes, 'queries':queries , 'others':others})
			except Exception as e:
				print 'Exception ', e
				return render(request, 'tasks/list_tasks.html', {'entries': entries, 'error': 1})
		else:
			return render(request, 'tasks/list_tasks.html')
	else:
		return render(request, 'tasks/login.html')

def search_tasks(request):
	#search in tasks by mask of comment
	if request.user.is_authenticated():
		if request.method == 'POST':
			user = request.user
			entries = {}
			try:
				criterion = request.POST['criterion']
				#print criterion
				entries = Tasks.objects.filter(comment__icontains=criterion).filter(login=user).order_by('-activity_date')
				print entries
				return render(request, 'tasks/list_tasks.html', {'entries': entries})
			#except DoesNotExist as e:
			#	print 'Exception ', e
			#	return render(request, 'tasks/list_tasks.html', {'entries': entries, 'error': 3})
			except Exception as e:
				#print 'Exception ', e
				logging.DEBUG('criterion %s' % criterion)
				logging.DEBUG(e)
				return render(request, 'tasks/list_tasks.html', {'entries': entries, 'error': 2})
		else:
			return render(request, 'tasks/list_tasks.html')
	else:
		return render(request, 'tasks/login.html')



def over_time(request):
	#method to add over_time
	if request.user.is_authenticated():
		if request.method == 'POST':
			user = request.user
			try:
				calendar = request.POST['calendar']
				calendar = datetime.strptime(calendar, '%d %B, %Y').date()
				comment = request.POST['comment']
				if (calendar is not None) and (comment is not None):
					try:
						insert = Over_Time(login=user, activity_date=calendar, comment=comment)
						insert.save()
						return render(request, 'tasks/over_time.html', {'entry_saved' : 1})
					except Exception as e:
						print 'Exception ', e
						return render(request, 'tasks/over_time.html', {'entry_saved' : 0})
			except Exception as e:
				print 'Exception ', e
				return render(request, 'tasks/over_time.html', {'entry_saved' : 0})
		else:
			calendar = None
			comment = None
			return render(request, 'tasks/over_time.html')
	else:
		return render(request, 'tasks/login.html')




def list_over_time(request):
	#method for list over time between dates
	if request.user.is_authenticated():
		if request.method == 'POST':
			user = request.user
			entries = {}
			try:
				calendar_start = request.POST['calendar_start']
				calendar_start = datetime.strptime(calendar_start, '%d %B, %Y').date()
				calendar_end = request.POST['calendar_end']
				calendar_end = datetime.strptime(calendar_end, '%d %B, %Y').date()
				entries = Over_Time.objects.filter(login=user).filter(activity_date__range=(calendar_start, calendar_end))
				return render(request, 'tasks/list_over_time.html', {'entries': entries})
			except Exception as e:
				print 'Exception ', e
				return render(request, 'tasks/list_over_time.html', {'entries': entries, 'dates': 1})
		else:
			return render(request, 'tasks/list_over_time.html')
	else:
		return render(request, 'tasks/login.html')


def post_work(request):
	return render(request, 'tasks/post_work.html')

def list_works(request):
	return render(request, 'tasks/list_works.html')
