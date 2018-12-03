
import itertools
from abc import ABC, abstractmethod

from django.utils.safestring import mark_safe
from django.forms.renderers import get_default_renderer
from django.template.exceptions import TemplateDoesNotExist


class VisualizationTemplate(ABC):
    id_counter = itertools.count()
    template_name = None

    def __init__(self, data=None):
        self.id = next(self.id_counter)
        if data is not None:
            self.set_data(data)

    def get_context(self, **kwargs):
        return {
            'div_id': kwargs.get('div_id', f'rank_{self.id}'),
            'div_kwargs': kwargs.get('div_kwargs', {})
        }

    def render(self, **kwargs):
        if self.template_name is None:
            raise TemplateDoesNotExist('No template_name set')
        renderer = get_default_renderer()
        context = self.get_context(**kwargs)
        return mark_safe(renderer.render(self.template_name, context))

    @abstractmethod
    def set_data(self, data):
        pass

    def __str__(self):
        return mark_safe(self.render())
