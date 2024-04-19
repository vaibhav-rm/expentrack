from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("delete-entry/<id>/", views.delete_entry, name="delete-entry")
]