# from django.shortcuts import render
from multiprocessing import context
from tempfile import template
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from mainapp import tasks as mainapp_tasks
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import (
LoginRequiredMixin,
PermissionRequiredMixin,
)
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import (
CreateView,
DeleteView,
DetailView,
ListView,
TemplateView,
UpdateView,
View
)
from config import settings
from mainapp import models as mainapp_models
from mainapp import forms as mainapp_forms
import logging
logger = logging.getLogger(__name__)


# class CoursesDetailView(TemplateView):
#     template_name = "mainapp/courses_detail.html"

#     def get_context_data(self, pk=None, **kwargs):
#         logger.debug("Yet another log message")
#         context = super(CoursesDetailView, self).get_context_data(**kwargs)
#         context["course_object"] = get_object_or_404(
#             mainapp_models.Courses, pk=pk
#         )
#         context["lessons"] = mainapp_models.Lesson.objects.filter(
#             course=context["course_object"]
#         )
#         context["teachers"] = mainapp_models.CourseTeachers.objects.filter(
#             course=context["course_object"]
#         )
#         if not self.request.user.is_anonymous:
#             if not mainapp_models.CourseFeedback.objects.filter(
#                 course=context["course_object"], user=self.request.user
#                     ).count():
#                         context["feedback_form"] = mainapp_forms.CourseFeedbackForm(
#                             course=context["course_object"], user=self.request.user
#                         )
#         context["feedback_list"] = mainapp_models.CourseFeedback.objects.filter(
#             course=context["course_object"]).order_by("-created", "-rating")[:5]
#         return context


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"

    
class NewsListView(ListView):
    template_name = 'mainapp/news_list.html'
    model = mainapp_models.News
    paginate_by = 5
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

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context["objects"] = mainapp_models.Courses.objects.all()[:7]
        return context


class CourseDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        logger.debug("Yet another log message")
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(
            mainapp_models.Courses, pk=pk
        )
        context["lessons"] = mainapp_models.Lesson.objects.filter(
            course=context["course_object"]
        )
        # context["teachers"] = mainapp_models.CourseTeachers.objects.filter(
        #     course=context["course_object"]
        # )
        if not self.request.user.is_anonymous:
            if not mainapp_models.CourseFeedback.objects.filter(
                course=context["course_object"], user=self.request.user
                    ).count():
                        context["feedback_form"] = mainapp_forms.CourseFeedbackForm(
                            course=context["course_object"], user=self.request.user
                        )
        context["feedback_list"] = mainapp_models.CourseFeedback.objects.filter(
            course=context["course_object"]).order_by("-created", "-rating")[:5]

        cached_feedback = cache.get(f"feedback_list_{pk}")
        if not cached_feedback:
            context["feedback_list"] = mainapp_models.CourseFeedback.objects.filter(
                course=context["course_object"]).order_by("-created", "-rating")[:5].select_related()
            cache.set(f"feedback_list_{pk}", context["feedback_list"], timeout=300)
        else:
            context['feedback_list'] = cached_feedback 
        return context



class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = mainapp_models.CourseFeedback
    form_class = mainapp_forms.CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string(
            "mainapp/includes/feedback_card.html", context={"item": self.object}
        )
        return JsonResponse({"card": rendered_card})


class LogView(TemplateView):
    template_name = "mainapp/log_view.html"

    def get_context_data(self, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        with open(settings.LOG_FILE, "r") as log_file:
            for i, line in enumerate(log_file):
                if i == 1000: 
                    break
                log_slice.insert(0, line) 
            context["log"] = "".join(log_slice)
        return context

class LogDownloadView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))


# class ContactsPageView(TemplateView):
#     template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"] = mainapp_forms.MailFeedbackForm(
                user=self.request.user
            )
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(
                f"mail_feedback_lock_{self.request.user.pk}"
            )
            if not cache_lock_flag:
                cache.set(
                    f"mail_feedback_lock_{self.request.user.pk}", "lock", timeout=300,)
                messages.add_message(self.request, messages.INFO, _("Message sended"))
                mainapp_tasks.send_feedback_mail.delay({
                        "user_id": self.request.POST.get("user_id"),
                        "message": self.request.POST.get("message"),
                }
                )
            else:
                messages.add_message(self.request, messages.WARNING, ("You can send only one message per 5 minutes"),)
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


# class CoursesView(TemplateView):
#     template_name = 'mainapp/courses_list.html'


# class DocsView(TemplateView):
#     template_name = 'mainapp/doc_site.html'


# class IndexView(TemplateView):
#     template_name = 'mainapp/index.html'


# class NewsView(TemplateView):
#     template_name = 'mainapp/news.html'

#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         context_data['object_list'] = [
#             {
#                 'title': 'Новость раз',
#                 'preview': 'Прквью для новости раз',
#                 'date': datetime.now()
#             }, {
#                 'title': 'Новость два',
#                 'preview': 'Прквью для новости два',
#                 'date': datetime.now()
#             }, {
#                 'title': 'Новость три',
#                 'preview': 'Прквью для новости три',
#                 'date': datetime.now()
#             }, {
#                 'title': 'Новость четыре',
#                 'preview': 'Прквью для новости четыре',
#                 'date': datetime.now()
#             }, {
#                 'title': 'Новость пять',
#                 'preview': 'Прквью для новости пять',
#                 'date': datetime.now()
#             }, {
#                 'title': 'Новость шесть',
#                 'preview': 'Прквью для новости шесть',
#                 'date': datetime.now()
#             }
#         ]
#         context_data['range'] = range(1, 5)
#         return context_data


# class NewsWithPaginatorView(NewsView):
#     def get_context_data(self, page, **kwargs):
#         context = super().get_context_data(page=page, **kwargs)
#         context["page_num"] = page
#         return context