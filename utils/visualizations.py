
import itertools
from abc import ABC, abstractmethod


class VisualizationTemplate(ABC):
    id_counter = itertools.count()

    def __init__(self, data):
        self.id = next(self.id_counter)
        if data is not None:
            self.set_data(data)

    @abstractmethod
    def render(self, div_id=None, div_kwargs=None):
        pass

    @abstractmethod
    def set_data(self, data):
        pass

    def _create_div(self, div_id, div_kwargs):
        if div_id is None:
            div_id = 'vis_' + str(self.id)
        params = ''
        if div_kwargs is not None:
            params = ' ' + ' '.join(
                [k + '="' + v + '"' for k, v in div_kwargs.items()])
        div = f'<div id="' + div_id + '"' + params + '></div>'
        return div, div_id
