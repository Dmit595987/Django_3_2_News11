from django import template
from news.models import Category

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.filter(news__isnull=False, news__is_published=True).distinct()


