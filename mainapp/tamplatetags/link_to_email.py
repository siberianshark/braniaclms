from atexit import register
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def link_to_email(value):
    return mark_safe(f"<a href='mailto:{value}'>{value}</a>")