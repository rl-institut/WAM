
import itertools
from abc import ABC, abstractmethod

from django.utils.safestring import mark_safe


class VisualizationTemplate(ABC):
    id_counter = itertools.count()

    def __init__(self):
        self.id = next(self.id_counter)

    @abstractmethod
    def render(self, **kwargs):
        pass

    @abstractmethod
    def set_data(self, data):
        pass

    def __str__(self):
        return mark_safe(self.render())
