from django import template
from django.db.models import Count, F

from store.models import Category

register = template.Library()


@register.inclusion_tag('store/include/_category_list.html')
def show_menu():
    categories = Category.objects.annotate(
        cnt=Count('products', filter=F('products__on_sale'))).filter(
            cnt__gt=0).order_by('order')
    return {'categories': categories}
