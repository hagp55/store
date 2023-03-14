from django import template

from store.models import Product

register = template.Library()


@register.simple_tag
def get_new_product():
    return Product.objects.filter(on_sale=True).order_by('-created_at')[:10]
