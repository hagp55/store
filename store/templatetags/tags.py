from django import template
from django.db.models import Count, F

from store.models import Tag

register = template.Library()


@register.inclusion_tag('store/include/_tag_list.html')
def get_tags():
    tags = Tag.objects.annotate(
        cnt_on_sale=Count('products', filter=F('products__on_sale'))).filter(
            cnt_on_sale__gt=0).order_by('-cnt_on_sale')
    return {"tags": tags}
