from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig
from django.views.decorators.cache import cache_page

app_name = MainappConfig.name

urlpatterns = [
    path('contacts/', views.ContactsView.as_view(), name="contacts"),
    path('docs/', views.DocSitePageView.as_view(), name="docs"),
    path('', views.MainPageView.as_view(), name="mainapp"),

    # News
    path("news/", views.NewsListView.as_view(), name="news"),
    path("news/create/", views.NewsCreateView.as_view(), name="news_create",),
    path("news/<int:pk>/detail",views.NewsDetailView.as_view(),name="news_detail",),
    path("news/<int:pk>/update",views.NewsUpdateView.as_view(),name="news_update",),
    path("news/<int:pk>/delete",views.NewsDeleteView.as_view(),name="news_delete",),

    # Courses
    path("courses/", cache_page(60 * 5)(views.CourseListView.as_view()), name="courses"),
    path("courses/<int:pk>/detail/", views.CourseDetailView.as_view(), name="courses_detail",),
    path("course_feedback/", views.CourseFeedbackFormProcessView.as_view(), name="course_feedback",),

    # Logs
    path('logs/', views.LogView.as_view(), name='log_view'),
    path("log_download/", views.LogDownloadView.as_view(), name="log_download"),
]
