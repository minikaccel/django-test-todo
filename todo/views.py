from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TodoForm
from .models import Todo


def main_page(request):
    return render(request, "todo/home.html", {})


def login_user(request):
    form = AuthenticationForm()
    if request.method == "GET":
        context = {
            "form": form
        }
        return render(request, "todo/login_user.html", context)
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            context = {
                "form": form,
                "error": "Username or Password didn`t match.`"
            }
            return render(request, "todo/login_user.html", context)
        else:
            login(request, user)
            return redirect("todo:current_todo")


def register_user(request):
    form = UserCreationForm()
    if request.method == "GET":
        context = {
            "form": form
        }
        return render(request, "todo/register_user.html", context)
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect("todo:current_todo")
        except IntegrityError:
            context = {
                "form": form,
                "error": "Username is already taken"
            }
            return render(request, "todo/register_user.html", context)
        else:
            context = {
                "form": form,
                "error": "Password didn`t match`"
            }
            return render(request, "todo/register_user.html", context)


@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("todo:main_page")


@login_required
def show_current_todos(request):
    todos = Todo.objects.filter(user=request.user, completed=False)
    context = {
        "todos": todos
    }
    return render(request, "todo/current_todos.html", context)


@login_required
def show_completed_todos(request):
    todos = Todo.objects.filter(user=request.user, completed=True)
    context = {
        "todos": todos
    }
    return render(request, "todo/completed_todos.html", context)


@login_required
def create_todo(request):
    form = TodoForm()
    if request.method == "GET":
        context = {
            "form": form
        }
        return render(request, "todo/create_todo.html", context)
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect("todo:current_todo")
        except ValueError:
            context = {
                "form": TodoForm(),
                "error": "Bad data passed in."
            }
            return render(request, "todo/create_todo.html", context)


@login_required
def todo_detail(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "GET":
        form = TodoForm(instance=todo)
        context = {
            "todo": todo,
            "form": form
        }
        return render(request, "todo/todo_detail.html", context)
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect("todo:current_todo")
        except ValueError:
            context = {
                "todo": todo,
                "form": form,
                "error": "Bad info..."
            }
            return render(request, "todo/todo_detail.html", context)


@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.completed_date = timezone.now()
        todo.completed = True
        todo.save()
        return redirect("todo:current_todo")


@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect("todo:current_todo")
