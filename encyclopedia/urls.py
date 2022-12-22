from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entries, name="entries"),
    path("search", views.search , name="search"),
    path("new", views.add_entry, name='new'),
    path("edit/<str:title>", views.edit_entry, name='edit'),
    path("random", views.random_entry, name="random_entry"),
]
