from multiprocessing import context
from tempfile import template
from django.http import HttpResponse
from django.views.generic import TemplateView
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.core.cache import cache
from django.contrib.auth.mixins import (
LoginRequiredMixin,
PermissionRequiredMixin,
)
import logging
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import (
CreateView,
DeleteView,
DetailView,
ListView,
TemplateView,
UpdateView,
)
from mainapp import models as mainapp_models
from mainapp import forms
# from mainapp import tasks as mainapp_tasks


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"

    
class NewsListView(ListView):
    template_name = 'mainapp/news_list.html'
    model = mainapp_models.News
    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'mainapp/news_form.html'
    model = mainapp_models.News
    fields = "__all__"

    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.add_news",)


class NewsDetailView(DetailView):
    template_name = 'mainapp/news_detail.html'
    model = mainapp_models.News


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'mainapp/news_form.html'
    model = mainapp_models.News
    fields = "__all__"
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.change_news",)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'mainapp/news_confirm_delete.html'
    model = mainapp_models.News
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.delete_news",)


class CourseListView(TemplateView):
    template_name = "mainapp/courses_list.html"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context["objects"] = mainapp_models.Courses.objects.all()[:7]
        return context


class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = mainapp_models.CourseFeedback
    form_class = forms.CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string(
            "mainapp/includes/feedback_card.html", context={"item": self.object}
        )
        return JsonResponse({"card": rendered_card})


class CourseDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        logging.debug("Yet another log message")
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context["courses_object"] = get_object_or_404(mainapp_models.Courses, pk=pk)
        context["lessons"] = mainapp_models.Lesson.objects.filter(course=context["courses_object"])
        context["teachers"] = mainapp_models.CourseTeacher.objects.filter(courses=context["courses_object"])
        if not self.request.user.is_anonymous:
            if not mainapp_models.CourseFeedback.objects.filter(
                course=context["courses_object"], user=self.request.user
            ).count():
                context["feedback_form"] = forms.CourseFeedbackForm(
                    course=context["courses_object"], user=self.request.user
                )

        cached_feedback = cache.get(f"feedback_list_{pk}")
        if not cached_feedback:
            context["feedback_list"] = (
                mainapp_models.CourseFeedback.objects.filter(course=context["courses_object"])
                .order_by("-created", "-rating")[:5]
                .select_related()
            )
            cache.set(f"feedback_list_{pk}", context["feedback_list"], timeout=300)  # 5 minutes

            # Archive object for tests --->
            import pickle

            with open(f"mainapp/fixtures/006_feedback_list_{pk}.bin", "wb") as outf:
                pickle.dump(context["feedback_list"], outf)
            # <--- Archive object for tests

        else:
            context["feedback_list"] = cached_feedback

        return context


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'