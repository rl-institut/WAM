
import os
from configobj import ConfigObj
from django import template

from wam.settings import WAM_APPS, BASE_DIR

register = template.Library()

labels = {
    app: ConfigObj(os.path.join(BASE_DIR, app, 'labels.cfg'))
    for app in WAM_APPS
}


@register.simple_tag(takes_context=True)
def label(context, value):
    """
    Tries to load label from app-specific labels.cfg file

    value can be a simple key or key-chain which will load value from nested
    dict
    """
    app = context.request.path.split('/')[1]
    if app == '':
        return None
    current = labels.get(app)
    if current is None:
        return None

    keys = value.split(':')
    for key in keys:
        current = current.get(key)
        if current is None:
            return None
    return current
