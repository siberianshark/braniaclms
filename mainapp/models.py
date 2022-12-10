from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class News(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    preamble = models.CharField(max_length=1024, verbose_name='Вступление')
    body = models.TextField(verbose_name='Содержимое')
    body_as_markdown = models.BooleanField(default=False, verbose_name='Разметка Markdown')

    created_at= models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')
    
    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        
    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
        
        
class CoursesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Courses(models.Model):
    objects = CoursesManager()
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость', default=0)
    
    created_at= models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')
    
    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        
    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
        
        
        
class Lesson(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name='Курс')
    num = models.PositiveIntegerField(default=0, verbose_name='Номер урока')
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    
    created_at= models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')
    
    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        
    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
        

class CourseTeacher(models.Model):
    courses = models.ManyToManyField(Courses)
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')
    
    created_at= models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'преподаватель'
        verbose_name_plural = 'преподаватели'
        
    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()
    

class CourseFeedback(models.Model):
    RATING = (
        (5, "⭐⭐⭐⭐⭐"), 
        (4, "⭐⭐⭐⭐"), 
        (3, "⭐⭐⭐"), 
        (2, "⭐⭐"),
        (1, "⭐")
    )
    course = models.ForeignKey(
        Courses, on_delete=models.CASCADE, verbose_name=_("Course")
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("User")
    )
    feedback = models.TextField(
    default =_("No feedback"), verbose_name =_("Feedback")
    )
    rating = models.SmallIntegerField(
    choices=RATING, default=5, verbose_name=_("Rating")
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} ({self.user})"
