from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name="contacts"),
    path('courses/', views.CoursesView.as_view(), name="courses"),
    path('docs/', views.DocsView.as_view(), name="docs"),
    path('', views.IndexView.as_view(), name="mainapp"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('news/', views.NewsView.as_view(), name="news"),
    path('news/<int:page>/', views.NewsWithPaginatorView.as_view(), name="news_paginator"),
]