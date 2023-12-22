from django.urls import path
from pages import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create_task/', views.create_task, name='create_task'),
    path('complete_task/<int:task_id>', views.complete_task, name='complete_task'),
    path('complete_all_tasks/', views.complete_all_tasks, name='complete_all_tasks'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task'),
    path('delete_active_tasks/', views.delete_active_tasks, name='delete_active_tasks'),
    path('delete_completed_tasks/', views.delete_completed_tasks, name='delete_completed_tasks'),
    path('edit_task/<int:task_id>', views.edit_task, name='edit_task'),
    path('profile/', views.profile, name='profile'),
    path('examples', views.examples, name='examples'),
]

