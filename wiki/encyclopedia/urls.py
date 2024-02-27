from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.title, name="title"),
    path("search/", views.search, name="query"),
    path("random/", views.random, name="random")
]
