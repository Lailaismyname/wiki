from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("create",views.create, name="create"),
    path("search", views.search, name="search"),
    path("edit/<str:page>", views.edit, name="edit"),
    path("<str:pagename>", views.entry, name="entry"),
    path("random",views.random,name="random")
]
