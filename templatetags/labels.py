
from django import template
from django.utils.safestring import mark_safe

from wam.settings import APP_LABELS

register = template.Library()


@register.simple_tag(takes_context=True)
def label(context, value, safe=False, app=None):
    """
    Tries to load label from app-specific labels.cfg file

    value can be a simple key or key-chain which will load value from nested
    dict
    """
    if app is None:
        try:
            app = context.request.path.split('/')[1]
        except AttributeError:
            raise AttributeError(
                'Current app could not be found. '
                'This may occur in widget templates as they do not return '
                'request object. In this case, you can set app manually.'
            )
    if app == '':
        return None
    current = APP_LABELS.get(app)
    if current is None:
        return None

    keys = value.split(':')
    for key in keys:
        current = current.get(key)
        if current is None:
            return None

    if safe:
        return mark_safe(current)
    return current
