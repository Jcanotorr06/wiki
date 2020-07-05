from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("index", views.index, name="index"),
    path("wiki/<str:entry_name>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("aleator", views.aleator, name="aleator"),
    path("wiki/edit/<str:entry_name>", views.edit, name="edit"),
    path("add", views.add, name="add")
]
