from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/completed', tasks_completed, name='tasks_completed'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/', detail_task, name='detail_task'),
    path('tasks/<int:task_id>/complete/', complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
]
