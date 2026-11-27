from django.urls import path

from . import views

app_name = "panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("password/", views.password_change, name="password"),
    path("users/", views.users, name="users"),
    path("users/add/", views.user_add, name="user_add"),
    path("users/<int:pk>/password/", views.user_password, name="user_password"),
    path("users/<int:pk>/toggle/", views.user_toggle, name="user_toggle"),
    path("<slug:slug>/", views.object_list, name="list"),
    path("<slug:slug>/add/", views.object_edit, name="add"),
    path("<slug:slug>/<str:pk>/", views.object_edit, name="edit"),
    path("<slug:slug>/<str:pk>/delete/", views.object_delete, name="delete"),
    path("<slug:slug>/<str:pk>/toggle/", views.toggle_active, name="toggle"),
]
