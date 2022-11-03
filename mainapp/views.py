# from django.shortcuts import render
from multiprocessing import context
from tempfile import template
from django.http import HttpResponse
from django.views.generic import TemplateView
from datetime import datetime

# Create your views here.

class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'
    
class CoursesView(TemplateView):
    template_name = 'mainapp/courses_list.html'
    
class DocsView(TemplateView):
    template_name = 'mainapp/doc_site.html'

class IndexView(TemplateView):
    template_name = 'mainapp/index.html'
    
class LoginView(TemplateView):
    template_name = 'mainapp/login.html'
    
class NewsView(TemplateView):
    template_name = 'mainapp/news.html'
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = [
            {
                'title': 'Новость раз',
                'preview': 'Прквью для новости раз',
                'date': datetime.now()
            },{
                'title': 'Новость два',
                'preview': 'Прквью для новости два',
                'date': datetime.now()
            },{
                'title': 'Новость три',
                'preview': 'Прквью для новости три',
                'date': datetime.now()
            },{
                'title': 'Новость четыре',
                'preview': 'Прквью для новости четыре',
                'date': datetime.now()
            },{
                'title': 'Новость пять',
                'preview': 'Прквью для новости пять',
                'date': datetime.now()
            },{
                'title': 'Новость шесть',
                'preview': 'Прквью для новости шесть',
                'date': datetime.now()
            }
        ]
        context_data['range'] = range(1, 5)
        return context_data
    
    
class NewsWithPaginatorView(NewsView):
    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page, **kwargs)
        context["page_num"] = page
        return context