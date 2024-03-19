# websites/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.db.models import Q  # Import the Q object
from .forms import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Index
from django.shortcuts import render
from .models import IndexCategory, Index
from datetime import datetime, timedelta

def input_index(request):
    index_form = InputIndexForm()

    if request.method == 'POST':
        if 'index_form_submit' in request.POST:
            index_form = InputIndexForm(request.POST, request.FILES)
            if index_form.is_valid():
                category = index_form.cleaned_data['category']
                new_category = index_form.cleaned_data['new_category']

                if not category and new_category:
                    # Create a new category if not selected from the dropdown
                    category, created = IndexCategory.objects.get_or_create(category_name=new_category)

                index_form.instance.category = category
                index_form.save()
                return redirect('/')

    context = {
        'index_form': index_form,
    }

    return render(request, 'websites/input_index.html', context)


def desktop(request):
    # Get all categories
    categories = IndexCategory.objects.all().order_by('category_order_num')

    # Create a dictionary to store indexes grouped by category
    indexes_by_category = {category: [] for category in categories}

    # Get all indexes and organize them by category
    indexes = Index.objects.all().order_by('website_index_position_num')
    for index in indexes:
        indexes_by_category[index.category].append(index)

    # Sort indexes within each category based on the website_index_position_num
    for category, indexes_list in indexes_by_category.items():
        indexes_list.sort(key=lambda x: x.website_index_position_num)

    # start
    # task list
    # original task list (list all not complete tasks)
    #     tasks = ToDoTask.objects.filter(task_done=False)
    # new code for task list : task not done, no due_date or due_date will be within 2 weeks
    # Get today's date
    today_date = datetime.now()
    # Filter tasks based on your conditions
    tasks = ToDoTask.objects.filter(task_done=False)
    total_tasks = tasks.count()

    # reminder tasks list
    # Get today's date and time
    today_date = timezone.now()
    # Filter reminder tasks based on conditions
    reminder_tasks = ToDoTask.objects.filter(task_done=False, task_reminder1_date__lte=today_date)
    total_reminder_tasks = reminder_tasks.count()
    # end

    # context or data to webpage
    context = {
        'indexes_by_category': indexes_by_category,
        'total_tasks': total_tasks,
        'total_reminder_tasks': total_reminder_tasks,
    }
    return render(request, 'websites/desktop.html', context)


def index_add_icon(request, pk):
    index = Index.objects.get(id=pk)
    index_form = InputIndexForm(instance=index)

    if request.method == 'POST':
        index_form = InputIndexForm(request.POST, request.FILES, instance=index)
        if index_form.is_valid():
            index_form.save()
            return redirect('/')

    context = {'index_form': index_form}

    return render(request, 'websites/index_add_icon.html', context)


def delete_index(request, pk):
    index = get_object_or_404(Index, id=pk)

    if request.method == "POST":
        confirmation_code = request.POST.get('confirmation_code')

        # Check if the confirmation code is valid (preset to 123)
        if confirmation_code == '123':
            index.delete_website_image()
            index.delete()
            return redirect('/')
        else:
            context = {
                'index': index,
                'msg': 'wrong delete code'
            }
            return render(request, 'websites/delete_index.html', context)

    context = {'index': index}
    return render(request, 'websites/delete_index.html', context)


def desktop_show_delete_symbol(request):
    # Get all categories
    categories = IndexCategory.objects.all().order_by('category_order_num')

    # Create a dictionary to store indexes grouped by category
    indexes_by_category = {category: [] for category in categories}

    # Get all indexes and organize them by category
    indexes = Index.objects.all().order_by('website_index_position_num')
    for index in indexes:
        indexes_by_category[index.category].append(index)

    # Sort indexes within each category based on the website_index_position_num
    for category, indexes_list in indexes_by_category.items():
        indexes_list.sort(key=lambda x: x.website_index_position_num)
    # context or data to webpage
    context = {
        'indexes_by_category': indexes_by_category,
        # 'total_tasks': total_tasks,
        # 'total_reminder_tasks': total_reminder_tasks,
    }
    return render(request, 'websites/desktop_show_delete_symbol.html', context)


@csrf_exempt
def update_order(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        order = request.POST.get('order').split(',')

        for position_num, index_id in enumerate(order, start=1):
            Index.objects.filter(id=index_id).update(website_index_position_num=position_num)
        return JsonResponse({'message': 'Order updated successfully'})

    return JsonResponse({'message': 'Invalid request'}, status=400)


def reorder_categories(request):
    if request.method == 'POST':
        new_order = request.POST.getlist('category_order[]')
        for idx, category_id in enumerate(new_order, start=1):
            category = IndexCategory.objects.get(pk=category_id)
            category.category_order_num = idx
            category.save()

        return JsonResponse({'success': True})

    categories = IndexCategory.objects.all().order_by('category_order_num')
    return render(request, 'websites/reorder_categories.html', {'categories': categories})


def index_list(request):
    categories = IndexCategory.objects.all().order_by('category_order_num')
    indexes_by_category = {}

    for category in categories:
        indexes_category = Index.objects.filter(category=category)
        indexes_by_category[category] = indexes_category

    indexes = Index.objects.all().order_by('-click_times')

    context = {
        'indexes_by_category': indexes_by_category,
        'indexes': indexes,
        # 'category_pk': category_pk,  # debug only
        #
        # 'tasks': tasks,
        # 'todotask_form': todotask_form,
        # 'total_tasks': total_tasks,
        # 'reminder_tasks': reminder_tasks,
    }

    return render(request, 'websites/index_list.html', context)


def update_index(request, pk):
    index = Index.objects.get(id=pk)
    index_form = InputIndexForm(instance=index)

    if request.method == 'POST':
        index_form = InputIndexForm(request.POST, request.FILES, instance=index)
        if index_form.is_valid():
            index_form.save()
            return redirect('/')

    context = {'index_form': index_form}

    return render(request, 'websites/input_index.html', context)


def input_todo_tasks(request):
    todotask_form = ToDoTaskForm()

    if request.method == 'POST':
        if 'todotask_form_submit' in request.POST:
            todotask_form = ToDoTaskForm(request.POST)
            if todotask_form.is_valid():
                todotask_form.save()
                return redirect('input_todo_tasks')

    # task list
    # original task list (list all not complete tasks)
    #     tasks = ToDoTask.objects.filter(task_done=False)
    # new code for task list : task not done, no due_date or due_date will be within 2 weeks
    # Get today's date
    today_date = datetime.now()
    # Filter tasks based on your conditions
    tasks = ToDoTask.objects.filter(Q(task_done=False)).order_by('-task_created_date')
    total_tasks = tasks.count()

    # reminder tasks list
    # Get today's date and time
    today_date = timezone.now()
    # Filter reminder tasks based on conditions
    reminder_tasks = ToDoTask.objects.filter(task_done=False, task_reminder1_date__lte=today_date)

    context = {
        'tasks': tasks,
        'todotask_form': todotask_form,
        'total_tasks': total_tasks,
        'reminder_tasks': reminder_tasks,
    }

    return render(request, 'websites/input_todo_tasks.html', context)


def mark_task_done(request, task_id):
    task = ToDoTask.objects.get(pk=task_id)
    task.task_done = True
    task.save()
    return redirect('input_todo_tasks')


def update_todo_task(request, pk):
    todotask = ToDoTask.objects.get(id=pk)
    tasks = ToDoTask.objects.filter(Q(task_done=False)).order_by('-task_created_date')

    if request.method == 'POST':
        todotask_form = ToDoTaskForm(request.POST, instance=todotask)
        if todotask_form.is_valid():
            todotask_form.save()
            return redirect('input_todo_tasks')

    else:
        todotask_form = ToDoTaskForm(instance=todotask)

    # reminder tasks list
    # Get today's date and time
    today_date = timezone.now()
    # Filter reminder tasks based on conditions
    reminder_tasks = ToDoTask.objects.filter(task_done=False, task_reminder1_date__lte=today_date)

    context = {
        'todotask_form': todotask_form,
        'todotask': todotask,  # Add this line to pass the instance to the template
        'tasks': tasks,
        'reminder_tasks': reminder_tasks,
    }

    return render(request, 'websites/input_todo_tasks.html', context)


# record click times, and click date time
@require_POST
def record_click(request):
    index_id = request.POST.get('index_id')
    if index_id:
        try:
            index = Index.objects.get(id=index_id)
            # Update last click date and increment click times
            index.last_click_date = timezone.now()
            index.click_times += 1
            index.save()
            return JsonResponse({'success': True})
        except Index.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Index not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Index ID not provided'})


# desktop show recent click above; and frequent click below 20 icons
def desktop_recent(request):

    # Get all indexes and organize them by category
    # indexes = Index.objects.all().order_by('-last_click_date')[:23]
    indexes = Index.objects.exclude(key_words="New").exclude(key_words="Delete").exclude(key_words="Reorder").order_by('-last_click_date')[:20]
    frequent_indexes = Index.objects.exclude(key_words="New").exclude(key_words="Delete").exclude(key_words="Reorder").order_by('-click_times')[:20]

    # start
    # task list
    # original task list (list all not complete tasks)
    #     tasks = ToDoTask.objects.filter(task_done=False)
    # new code for task list : task not done, no due_date or due_date will be within 2 weeks
    # Get today's date
    today_date = datetime.now()
    # Filter tasks based on your conditions
    tasks = ToDoTask.objects.filter(task_done=False)
    total_tasks = tasks.count()

    # reminder tasks list
    # Get today's date and time
    today_date = timezone.now()
    # Filter reminder tasks based on conditions
    reminder_tasks = ToDoTask.objects.filter(task_done=False, task_reminder1_date__lte=today_date)
    total_reminder_tasks = reminder_tasks.count()
    # end

    # context or data to webpage
    context = {
        'indexes': indexes,
        'frequent_indexes': frequent_indexes,
        'total_tasks': total_tasks,
        'total_reminder_tasks': total_reminder_tasks,
    }
    return render(request, 'websites/desktop_show_recent_icons.html', context)


# show category "work" only
def desktop_work_only(request):
    # Filter categories to include only "Work" and "News"
    categories = IndexCategory.objects.filter(category_name__in=["Work",]).order_by('category_order_num')

    # Create a dictionary to store indexes grouped by category
    indexes_by_category = {category: [] for category in categories}

    # Get all indexes and organize them by category
    indexes = Index.objects.all().order_by('website_index_position_num')
    for index in indexes:
        if index.category in indexes_by_category:
            indexes_by_category[index.category].append(index)

    # Sort indexes within each category based on the website_index_position_num
    for category, indexes_list in indexes_by_category.items():
        indexes_list.sort(key=lambda x: x.website_index_position_num)

    # Task list
    # Get today's date
    today_date = datetime.now()
    # Filter tasks based on your conditions
    tasks = ToDoTask.objects.filter(task_done=False)
    total_tasks = tasks.count()

    # Reminder tasks list
    # Get today's date and time
    today_date = timezone.now()
    # Filter reminder tasks based on conditions
    reminder_tasks = ToDoTask.objects.filter(task_done=False, task_reminder1_date__lte=today_date)
    total_reminder_tasks = reminder_tasks.count()

    # Context data to webpage
    context = {
        'indexes_by_category': indexes_by_category,
        'total_tasks': total_tasks,
        'total_reminder_tasks': total_reminder_tasks,
    }
    return render(request, 'websites/desktop.html', context)
