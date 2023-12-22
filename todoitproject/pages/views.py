from django.shortcuts import render, redirect
from tasks.models import Task
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
    context = {
        'tasks': tasks,
    }
    return render(request, 'pages/index.html', context=context)

@login_required
def create_task(request):
    if request.method == 'POST':
        user = request.user
        new_task = Task()
        if 'title' in request.POST:
            new_task.title = request.POST['title']
        if 'description' in request.POST:
            new_task.description = request.POST['description']
        if 'priority' in request.POST:
            new_task.priority = request.POST['priority']
        new_task.user = user
        new_task.save()
        messages.success(request, 'Task #{} successfully created!'.format(new_task.id))
        return redirect('index')

@login_required
def complete_task(request, task_id):
    user = request.user
    task = Task.objects.get(id=task_id, user=user)
    task.is_completed = not task.is_completed
    task.save()
    messages.success(request, 'Task #{} successfully completed!'.format(task.id))
    return redirect('index')

@login_required
def complete_all_tasks(request):
    user = request.user
    tasks = Task.objects.filter(is_completed=False).filter(user=user)
    for task in tasks:
        task.is_completed = True
        task.save()
    messages.success(request, 'All Tasks successfully completed!')
    return redirect('index')

@login_required
def delete_task(request, task_id):
    user = request.user
    task = Task.objects.get(id=task_id, user=user)
    task.delete()
    messages.warning(request, 'Task #{} successfully deleted!'.format(task.id))
    return redirect('index')

@login_required
def delete_active_tasks(request):
    user = request.user
    tasks = Task.objects.filter(is_completed=False).filter(user=user)
    for task in tasks:
        task.delete()
    messages.warning(request, 'All Active Tasks successfully deleted!')
    return redirect('index')

@login_required
def delete_completed_tasks(request):
    user = request.user
    tasks = Task.objects.filter(is_completed=True).filter(user=user)
    for task in tasks:
        task.delete()
    messages.warning(request, 'All Completed Tasks successfully deleted!')
    return redirect('index')

@login_required
def edit_task(request, task_id):
    user = request.user
    task = Task.objects.get(id=task_id, user=user)
    context = {
        'task': task,
    }
    if request.method == 'GET':
        return render(request, 'pages/edit_task.html', context=context)
    
    if request.method == 'POST':
        if 'title' in request.POST:
            task.title = request.POST['title']
        if 'description' in request.POST:
            task.description = request.POST['description']
        if 'priority' in request.POST:
            task.priority = request.POST['priority']
        task.save()
        messages.success(request, 'Task #{} successfully updated!'.format(task.id))
        return redirect('index')

@login_required
def profile(request):
    user=request.user
    tasks = Task.objects.filter(user=user)
    context = {
        'active_tasks': tasks.filter(is_completed=False).count(),
        'completed_tasks': tasks.filter(is_completed=True).count(),
        }
    return render(request, 'pages/profile.html', context=context)

def examples(request):
    context = {
        'friends': ['Deadpool', 'Batman', 'Superman'],
        'demo': 'this is a demo',
        'dict_example': {
            'name': 'Nick',
            'lastname': 'Jones',
            'age': 23,
            'hobbies': [
                'programming',
                'hockey',
                'art'
                ]
            }
        }
    return render(request, 'pages/examples.html', context=context)