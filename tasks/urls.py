from django.conf.urls import include, url
from . import views


#bindings of url and view
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^settings/$', views.settings, name='settings'),
	url(r'^change_password/$', views.change_password, name='change_password'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^post_task/$', views.post_task, name='post_task'),
	url(r'^list_tasks/$', views.list_tasks, name='list_tasks'),
	url(r'^search_tasks/$', views.search_tasks, name='search_tasks'),
	url(r'^over_time/$', views.over_time, name='over_time'),
	url(r'^list_over_time/$', views.list_over_time, name='list_over_time'),
	url(r'^post_work/$', views.post_work, name='post_work'),
	url(r'^list_works/$', views.list_works, name='list_works'),
	url(r'^search_works/$', views.search_works, name='search_works'),
	url(r'^add_to_do/$', views.add_to_do, name='add_to_do'),
	url(r'^edit_to_do/$', views.edit_to_do, name='edit_to_do'),
	url(r'^list_to_do/$', views.list_to_do, name='list_to_do'),
]
