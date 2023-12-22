# contents of tasks/tests/test_views.py
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from tasks.models import Task
from django.contrib.messages import get_messages

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def logged_in_client(client, user):
    client.force_login(user)
    return client

@pytest.fixture
def task(db, user):
    return Task.objects.create(
        title="Test Task",
        description="Test Description",
        priority="Low",
        user=user
    )

@pytest.fixture
def create_multiple_tasks(task):
    Task.objects.create(title="Second Task", description="Another task", user=task.user)
    completed_task = Task.objects.create(
        title="Completed Task", 
        description="Completed task description", 
        user=task.user,
        is_completed=True
    )
    return completed_task

def test_index_view(logged_in_client):
    url = reverse('index')
    response = logged_in_client.get(url)
    assert response.status_code == 200
    assert "tasks" in response.context

def test_create_task_view(logged_in_client):
    url = reverse('create_task')
    data = {'title': 'New Task', 'description': 'Do something', 'priority': 'Medium'}
    response = logged_in_client.post(url, data)
    
    assert Task.objects.count() == 1
    assert response.status_code == 302
    assert response.url == reverse('index')

def test_complete_task_view(logged_in_client, task):
    url = reverse('complete_task', args=[task.id])
    response = logged_in_client.get(url)
    task.refresh_from_db()
    
    assert task.is_completed
    assert response.status_code == 302
    assert response.url == reverse('index')

def test_edit_task_get(logged_in_client, task):
    url = reverse('edit_task', args=[task.id])
    response = logged_in_client.get(url)
    
    assert response.status_code == 200
    assert response.context['task'].id == task.id

def test_edit_task_post(logged_in_client, task):
    url = reverse('edit_task', args=[task.id])
    updated_data = {'title': 'Updated Title', 'description': 'Updated Description', 'priority': 'High'}
    response = logged_in_client.post(url, updated_data)
    task.refresh_from_db()
    
    assert task.title == 'Updated Title'
    assert task.description == 'Updated Description'
    assert task.priority == 'High'
    assert len(list(get_messages(response.wsgi_request))) == 1
    assert response.status_code == 302
    assert response.url == reverse('index')

def test_complete_all_tasks_view(logged_in_client, user, create_multiple_tasks):
    url = reverse('complete_all_tasks')
    response = logged_in_client.get(url)
    tasks = Task.objects.filter(user=user)
    
    assert all(task.is_completed for task in tasks)
    assert response.status_code == 302
    assert response.url == reverse('index')

def test_delete_task_view(logged_in_client, task):
    url = reverse('delete_task', args=[task.id])
    response = logged_in_client.get(url)
    
    assert response.status_code == 302
    assert response.url == reverse('index')
    assert not Task.objects.filter(pk=task.pk).exists()

def test_delete_active_tasks_view(logged_in_client, user, create_multiple_tasks):
    url = reverse('delete_active_tasks')
    response = logged_in_client.get(url)
    
    assert Task.objects.filter(user=user, is_completed=False).count() == 0
    assert Task.objects.filter(user=user, is_completed=True).exists()
    assert response.status_code == 302
    assert response.url == reverse('index')

def test_delete_completed_tasks_view(logged_in_client, user, create_multiple_tasks):
    url = reverse('delete_completed_tasks')
    response = logged_in_client.get(url)
    
    assert Task.objects.filter(user=user, is_completed=True).count() == 0
    assert Task.objects.filter(user=user, is_completed=False).exists()
    assert response.status_code == 302
    assert response.url == reverse('index')

def test_profile_view(logged_in_client, task):
    task.is_completed = True
    task.save()
    Task.objects.create(title="Active Task", description="Active task description", user=task.user)
    
    url = reverse('profile')
    response = logged_in_client.get(url)
    
    assert response.status_code == 200
    assert response.context['active_tasks'] == 1
    assert response.context['completed_tasks'] == 1
