from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task

from .forms import TaskForm

# Create your views here.

# Function for user signup
def signup(request):
    '''Handles user signup. If the request method is 'GET', renders the signup.html template
    with the UserCreationForm. If the request method is 'POST', creates a new user with the
    provided username and password, and logs in the user. If there's an error, renders the
    signup.html template with an appropriate error message.'''
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:
        # Handle POST request for user signup
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})


# Function to display the tasks for the logged-in user
@login_required
def tasks(request):
    '''Retrieves all tasks for the logged-in user that are not completed (datecompleted is null).
    Renders the tasks.html template with the retrieved tasks.'''
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})


# Function to display the completed tasks for the logged-in user
@login_required
def tasks_completed(request):
    '''Retrieves all completed tasks for the logged-in user and orders them by datecompleted in
    descending order. Renders the tasks.html template with the retrieved completed tasks.'''
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})


# Function to create a new task for the logged-in user
@login_required
def create_task(request):
    '''Handles the creation of a new task for the logged-in user. If the request method is 'GET',
    renders the create_task.html template with an empty TaskForm to create a new task. If the
    request method is 'POST', saves the new task associated with the logged-in user. If there's an
    error, renders the create_task.html template with an appropriate error message.'''
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})


# Function to display the home page
def home(request):
    '''Renders the home.html template.'''
    return render(request, 'home.html')


# Function to sign out the current user
@login_required
def signout(request):
    '''Logs out the current user and redirects to the home page.'''
    logout(request)
    return redirect('home')


# Function for user sign-in
def signin(request):
    '''Handles user sign-in. If the request method is 'GET', renders the signin.html template
    with the AuthenticationForm to log in. If the request method is 'POST', authenticates the
    user with the provided username and password. If the authentication fails, renders the
    signin.html template with an appropriate error message. If successful, logs in the user and
    redirects to the tasks page.'''
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('tasks')


# Function to view the details of a specific task for the logged-in user
@login_required
def task_detail(request, task_id):
    '''Handles the viewing and updating of a specific task for the logged-in user. If the request
    method is 'GET', retrieves the task with the given task_id that belongs to the logged-in user.
    Renders the task_detail.html template with the retrieved task and its TaskForm. If the request
    method is 'POST', updates the task details and redirects to the tasks page. If there's an
    error, renders the task_detail.html template with an appropriate error message.'''
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})


# Function to mark a specific task as completed for the logged-in user


@login_required
def complete_task(request, task_id):
    '''Handles marking a specific task with the given task_id as completed for the logged-in user.
    Retrieves the task with the provided task_id that belongs to the logged-in user. If the request
    method is 'POST', sets the completion date to the current date and time, saves the updated task,
    and redirects to the tasks page.'''
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


# Function to delete a specific task for the logged-in user
@login_required
def delete_task(request, task_id):
    '''Handles deleting a specific task with the given task_id for the logged-in user. Retrieves the
    task with the provided task_id that belongs to the logged-in user. If the request method is 'POST',
    deletes the task and redirects to the tasks page.'''
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
