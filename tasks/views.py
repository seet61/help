from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts  import redirect
from datetime import datetime, date
from django.contrib.auth.models import User
#from django.core.exceptions import DoesNotExist

from .models import Tasks, Over_Time, Works, ToDo
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
                    logger.info('Changing password for %s' % user)
                    if ((authenticate(username=user, password=current_password)) is not None):
                        u = User.objects.get(username=user)
                        u.set_password(new_password)
                        u.save()
                        return render(request, 'tasks/settings.html', {'password_changed' : 1})
                    else:
                        logger.error('Bad data for changing password for %s' % user)
                        return render(request, 'tasks/settings.html', {'bad_data' : 1})
                else:
                    logger.error('Bad cofirm for changing password for %s' % user)
                    return render(request, 'tasks/settings.html', {'bad_confirm' : 1})
            except Exception as e:
                logger.error('Bad data for changing password for %s' % user)
                logger.error(e.message)
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
        user = request.user
        logging.info('User %s is logout' % user)
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
                        #print 'len ', len(entry)
                        if len(entry) != 0:
                            return render(request, 'tasks/post_task.html', {'task_saved' : 2})
                        else:
                            insert = Tasks(number=number, login=user, activity_date=calendar, comment=comment)
                            insert.save()
                            logger.info('Task %s was saved for user %s' % (number, user))
                            return render(request, 'tasks/post_task.html', {'task_saved' : 1})
                    except Exception as e:
                        #print 'Exception ', e
                        logger.error('Task %s was saved for user %s, %s, %s' % (number, user, calendar, comment))
                        logger.error(e)
                        return render(request, 'tasks/post_task.html', {'task_saved' : 0})
                else:
                    return render(request, 'tasks/post_task.html')
            except Exception as e:
                #print 'Exception ', e
                logger.error('Task %s wasn''t saved for user %s, %s, %s' % (number, user, calendar, comment))
                logger.error(e)
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
                if len(calendar_end) > 0:
                    calendar_end = datetime.strptime(calendar_end, '%d %B, %Y').date()
                else:
                    calendar_end = datetime.today().date() 
                if calendar_start > calendar_end:
                    return render(request, 'tasks/list_tasks.html', {'entries': entries, 'error': 0})   
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
                logger.info('List tasks for user %s' % user)
                return render(request, 'tasks/list_tasks.html', {'changes': changes, 'queries':queries , 'others':others})
            except Exception as e:
                #print 'Exception ', e
                logger.error('Cann''t get list of tasks for %s' % user)
                logger.error(e)
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
                logger.info('Searching task for criterion: %s' % criterion)
                entries = Tasks.objects.filter(comment__icontains=criterion).filter(login=user).order_by('-activity_date')
                return render(request, 'tasks/list_tasks.html', {'entries': entries})
            except Exception as e:
                logging.DEBUG('criterion %s' % criterion)
                logging.DEBUG(e)
                logger.error(e)
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
                        logging.info('Overtime for %s was saved' % user)
                        return render(request, 'tasks/list_over_time.html', {'entry_saved' : 1})
                    except Exception as e:
                        logging.info('Overtime for %s wasn''t saved' % user)
                        logger.error(e)
                        return render(request, 'tasks/list_over_time.html', {'entry_saved' : 0})
            except Exception as e:
                return render(request, 'tasks/over_time.html', {'entry_saved' : 0})
        else:
            calendar = None
            comment = None
            return render(request, 'tasks/list_over_time.html')
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
                #print len(calendar_end)
                if len(calendar_end) > 0:
                    calendar_end = datetime.strptime(calendar_end, '%d %B, %Y').date()
                else:
                    calendar_end = datetime.today().date()               
                print calendar_start, calendar_end
                if calendar_start > calendar_end:
                    return render(request, 'tasks/list_over_time.html', {'entries': entries, 'dates': 0})
                entries = Over_Time.objects.filter(login=user).filter(activity_date__range=(calendar_start, calendar_end))
                logger.info('List overtime for %s' % user)
                return render(request, 'tasks/list_over_time.html', {'entries': entries})
            except Exception as e:
                logger.error('Cann''t get list of overtime for %s' % user)
                logger.error(e)
                return render(request, 'tasks/list_over_time.html', {'entries': entries, 'error': 1})
        else:
            return render(request, 'tasks/list_over_time.html')
    else:
        return render(request, 'tasks/login.html')


def post_work(request):
    #method to add information about work
    if request.user.is_authenticated():
        if request.method == 'POST':
            user = request.user
            try:
                number = request.POST['number']
                date = request.POST['calendar']
                if date != '':
                    date = datetime.strptime(date, '%d %B, %Y').date()
                else:
                    return render(request, 'tasks/post_work.html', {'entry_saved' : 0})
                if (request.POST.__contains__('switch_field')):
                    switch_field = True
                else:
                    switch_field = False
                installed = request.POST['installed']
                restarted = request.POST['restarted']
                passwords = request.POST['passwords']
                logs = request.POST['log_dirs']
                problems = request.POST['problems']
                if (request.POST.__contains__('call_CC')):
                    call_CC = True
                    time_CC = request.POST['time_CC']
                    if time_CC != '':
                        time_CC = datetime.strptime(time_CC, '%H:%M').time()
                else:
                    call_CC = False
                    time_CC = datetime.strptime('00:00', '%H:%M').time()
                if (request.POST.__contains__('whatsapp')):
                    whatsapp = True
                else:
                    whatsapp = False
                if (request.POST.__contains__('sms')):
                    sms = True
                else:
                    sms = False
                comment = request.POST['comment']
                try:
                    insert = Works(number=number, login=user, activity_date=date, field=switch_field,
                            installed=installed, restarted=restarted, passwords_users=passwords, 
                            logs=logs, problems=problems, call_CC=call_CC, time_CC=time_CC, 
                            whatsapp=whatsapp, sms=sms, comment=comment)
                    insert.save()
                    logger.info('Work for %s was saved' % user)
                    return render(request, 'tasks/post_work.html', {'entry_saved' : 1})
                except Exception as e:
                    logger.error('Cann''t save work for %s' % user)
                    logger.error(e)
                    return render(request, 'tasks/post_work.html', {'entry_saved' : 2})
            except Exception as e:
                logger.error('Cann''t save work for %s' % user)
                logger.error(e)
                return render(request, 'tasks/post_work.html', {'entry_saved' : 2})
        else:
            return render(request, 'tasks/post_work.html')
    else:
        return render(request, 'tasks/post_work.html')

def list_works(request):
    #method for list works between days
    if request.user.is_authenticated():
        if request.method == 'POST':
            user = request.user
            works = []
            try:
                calendar_start = request.POST['calendar_start']
                calendar_start = datetime.strptime(calendar_start, '%d %B, %Y').date()
                calendar_end = request.POST['calendar_end']
                if len(calendar_end) > 0:
                    calendar_end = datetime.strptime(calendar_end, '%d %B, %Y').date()
                else:
                    calendar_end = datetime.today().date()               
                if (request.POST.__contains__('switch_field')):
                    switch_field = True
                else:
                    switch_field = False
                if calendar_start > calendar_end:
                    logger.warning('Can''t get list of works for %s, because %s more than %s' % (user. calendar_start, calendar_end))
                    return render(request, 'tasks/list_works.html', {'works': works, 'error': 0})   
                works = Works.objects.filter(activity_date__range=(calendar_start, calendar_end)).filter(field=switch_field).order_by('-activity_date')
                logger.info('List works for %s' % user)
                return render(request, 'tasks/list_works.html', {'works': works})
            except Exception as e:
                logger.error('Cann''t get list of works for %s' % user)
                logger.error(e)
                return render(request, 'tasks/list_works.html', {'works': works, 'error': 1})
        else:
            return render(request, 'tasks/list_works.html')
    else:
        return render(request, 'tasks/login.html')

def search_works(request):
    #search in works by mask of comment
    if request.user.is_authenticated():
        if request.method == 'POST':
            entries = {}
            try:
                criterion = request.POST['criterion']
                works = Works.objects.filter(installed__icontains=criterion).order_by('-activity_date')
                #works = works.append(Works.objects.filter(restarted__icontains=criterion).order_by('-activity_date'))
                logger.info('Search works for %s with criterion: %s' % (user, criterion))
                return render(request, 'tasks/list_works.html', {'works': works})
            except Exception as e:
                logging.DEBUG('criterion %s' % criterion)
                logging.DEBUG(e)
                logger.error(e)
                return render(request, 'tasks/list_works.html', {'works': works, 'error': 2})
        else:
            return render(request, 'tasks/list_works.html')
    else:
        return render(request, 'tasks/login.html')

def add_to_do(request):
    #method to add information about what need to do
    if request.user.is_authenticated():
        if request.method == 'POST':
            try:
                target = request.POST['target']
                reason = request.POST['reason']
                startdate = request.POST['startdate']
                if len(startdate) > 0:
                    startdate = datetime.strptime(startdate, '%d %B, %Y').date()
                else:
                    startdate = datetime.today().date()     
                enddate = request.POST['enddate']
                if len(enddate) > 0:
                    enddate = datetime.strptime(enddate, '%d %B, %Y').date()
                else:
                    enddate = datetime.today().date()    
                try:
                    insert = ToDo(target=target, reason=reason, startdate=startdate, enddate=enddate)
                    insert.save()
                    logger.info('Add %s in to do list' % target)
                    return redirect('/tasks/list_to_do/1')
                except Exception as e:
                    logger.error('Cann''t add %s in to do list' % target)
                    logger.error(e)
                    print e.decode('utf8')
                    return redirect('/tasks/list_to_do/0')
            except Exception as e:
                logger.error('Cann''t add %s in to do list' % target)
                logger.error(e)
                return redirect('/tasks/list_to_do/0')
    else:
        return render(request, 'tasks/list_to_do.html')
    

def edit_to_do(request):
    #method for edit list to do
    if request.user.is_authenticated():
        for key, value in request.POST.iteritems():
            if '_checkbox' in key:
                try:
                    key = key.split('_checkbox')[0]
                    #print key
                    logger.info('Update entry %s ' % key)
                    ToDo.objects.filter(target=key).update(finished=True)
                    logger.info('Entry to do %s was marked as finished' % key)
                except Exception as e:
                    logger.error('Entry to do %s wasn''t marked as finished' % key)
                    logger.error(e)
                    return redirect('/tasks/list_to_do/3')
        return redirect('/tasks/list_to_do/2')
    else:
        return render(request, 'tasks/login.html')

def list_to_do(request, entry_saved=-1):
    #method for list to do
    if request.user.is_authenticated():
        entries = []
        try:
            todos = ToDo.objects.filter(finished=False)
            return render(request, 'tasks/list_to_do.html', {'entries': todos, 'entry_saved': int(entry_saved)})
        except Exception as e:
            logger.error('Can''t load list to do')
            logger.error(e)
            return render(request, 'tasks/list_to_do.html', {'entries': todos, 'error': 4})
    else:
        return render(request, 'tasks/login.html')
    
