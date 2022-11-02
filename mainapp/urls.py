from django.urls import path

from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('', views.NewsPageView.as_view()),
    path('', views.CoursesPageView.as_view()),
    path('', views.ContactsPageView.as_view()),
    path('', views.DocSitePageView.as_view()),
    path('', views.LoginPageView.as_view()),
]