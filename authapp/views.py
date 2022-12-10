from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from authapp import models
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from django.contrib.auth import get_user_model
from authapp import forms
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView


class ProfileEditView(UserPassesTestMixin, UpdateView):
    template_view = 'authapp/profile_edit.html'
    model = get_user_model()
    form_class = forms.CustomUserChangeForm

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("authapp:profile_edit", args=[self.request.user.pk])

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    template_name = "authapp/customuser_form.html"
    model = get_user_model()
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy("mainapp:mainapp")
    


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _("See you later!"))
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'

    def form_valid(self, form):
        ret = super().form_valid(form)
        message = _("Login success!<br>Hi, %(username)s") % {
            "username": self.request.user.get_full_name()
            if self.request.user.get_full_name()
            else self.request.user.get_username()
        }
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))