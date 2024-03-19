# project urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from websites.views import *


def home(request):
    return HttpResponse('Hello! Home page.')  # show hello on home page


def urls_list(request):
    return render(request, 'urls_list.html', {})  # templates/urls_list.html


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('urls_list/', urls_list, name='urls_list'),

    # website homepage setting:
    path('', desktop, name='desktop'),

    # index
    path('input_index/', input_index, name='input_index'),

    path('index_list/', index_list, name='index_list'),  # show index list
    path('desktop/', desktop, name='desktop'),  # show index icons
    path('index_add_icon/<str:pk>', index_add_icon, name='index_add_icon'),  # add icon for index
    path('desktop_show_delete_symbol/', desktop_show_delete_symbol, name='desktop_show_delete_symbol'),  # show index with delete symbol
    path('delete_index/<str:pk>', delete_index, name='delete_index'),  # delete index
    path('update_order/', update_order, name='update_order'),
    path('update_index/<str:pk>', update_index, name="update_index"),
    path('desktop_recent/', desktop_recent, name="desktop_recent"),
    path('desktop_work_only/', desktop_work_only, name="desktop_work_only"),

    path('reorder_categories/', reorder_categories, name='reorder_categories'),

    path('input_todo_tasks/', input_todo_tasks, name='input_todo_tasks'),
    path('mark_task_done/<int:task_id>/', mark_task_done, name='mark_task_done'),
    path('update_todo_task/<str:pk>/', update_todo_task, name='update_todo_task'),

    path('record_click/', record_click, name='record_click'),  # record click time and click date time
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
