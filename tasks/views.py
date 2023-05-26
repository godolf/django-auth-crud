from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'auth/signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Registrar user
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user) # crea la sesión
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'auth/signup.html', {
                    'form': UserCreationForm,
                    'error': 'Ups! Este usuario ya existe.'
                })
        else:
            return render(request, 'auth/signup.html', {
                'form': UserCreationForm,
                'error': 'Las contraseñas no coinciden.'
            })
        
def signin(request):
    if request.method == 'GET':
        return render(request, 'auth/signin.html', {
            'form': AuthenticationForm
        })
    else:
        try:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'auth/signin.html', {
                    'form': AuthenticationForm,
                    'error': 'Ups! Usuario o contraseña incorrectos.'
                })
            else:
                login(request, user)
                return redirect('tasks')
        except:
            return render(request, 'auth/signin.html', {
                'form': AuthenticationForm,
                'error': 'Ups! Algo ha ido mal.'
            })

@login_required
def signout(request):
    logout(request)
    return redirect('index')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull = True)
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull = False).order_by('-datecompleted')
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/create_task.html', {
                'form': TaskForm,
                'error': 'Ups! Algo ha ido mal.'
            })

@login_required
def detail_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':    
        form = TaskForm(instance=task)

        return render(request, 'tasks/detail_task.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/detail_task.html', {
            'task': task,
            'form': form,
            'error': 'Ups! Algo ha ido mal.'
        })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        if task.datecompleted == None:
            task.datecompleted = timezone.now()
            task.save()
        else:
            task.datecompleted = None
            task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        
    return redirect('tasks')
    