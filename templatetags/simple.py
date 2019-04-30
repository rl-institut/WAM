
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def index(current_list, i):
    return current_list[int(i)]
