from django.urls import path
from . import views


app_name = "todo"


urlpatterns = [
    path('register/', views.register_user, name="register_user"),
    path("login/", views.login_user, name="login_user"),
    path('logout/', views.logout_user, name="logout_user"),

    # Application
    path('', views.main_page, name="main_page"),
    path("create/", views.create_todo, name="create_todo"),
    path("current/", views.show_current_todos, name="current_todo"),
    path("completed/", views.show_completed_todos, name="completed_todo"),
    path('todo/<int:todo_pk>', views.todo_detail, name="todo_detail"),
    path("todo/<int:todo_pk>/complete",
         views.complete_todo, name="complete_todo"),
    path("todo/<int:todo_pk>/delete", views.delete_todo, name="delete_todo"),
]
