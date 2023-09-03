from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:name>',views.entries, name= 'entries'),
    path("Search/", views.Searcher, name="Searcher"),
    path("newpage/", views.newpage, name="newpage"),
    path("Modify/", views.modify, name="Modify"),
    path("edit/", views.editentry, name="edit"),
    path("random/", views.random, name="randompage"),
]
