from blog_app.models import Category, Favorite, Storage
from django import template
import json

register = template.Library()


@register.simple_tag()
def blog_categories():
    return Category.objects.all()


@register.simple_tag()
def blog_favorite(request):
    try:
        return Favorite.objects.get(user=request.user)
    except Exception:
        favorite_create = Favorite.objects.create(user=request.user)
        return favorite_create.save()



@register.simple_tag()
def blog_storage(request):
    lst = []
    for i in Storage.objects.filter(user=request.user):
        lst.append(i.product)
        lst.append(i.product_color)
    return lst


