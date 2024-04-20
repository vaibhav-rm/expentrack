from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("delete-entry/<id>/", views.delete_entry, name="delete-entry"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register")
]