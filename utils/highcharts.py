
import pandas
import json
from collections import namedtuple, ChainMap
from functools import reduce
from warnings import warn

from django.utils.safestring import mark_safe

from utils.visualizations import VisualizationTemplate

HC_Renderer = namedtuple('HighchartsRenderer', ['div', 'script'])


hc_kwargs = {
    'style': ['chart', 'type'],
    'title': ['title', 'text'],
    'subtitle': ['subtitle', 'text'],
    'renderTo': ['chart', 'renderTo'],
    'x_title': ['xAxis', 'title', 'text'],
    'y_title': ['yAxis', 'title', 'text'],
    'stacked': ['plotOptions', 'series', 'stacking'],
}


RLI_THEME = {
  'colors': [
      '#fc8e65', '#55aae5', '#7fadb7', '#fce288', '#f69c3a', '#c28e5e',
      '#a27b82', '#797097'
  ],
  'title': {
      'style': {
          'color': '#002E4F',
          'font': 'bold 1.2rem "Trebuchet MS", Verdana, sans-serif'
      }
  },
  'subtitle': {
      'style': {
          'color': '#666',
          'font': 'bold 12px "Trebuchet MS", Verdana, sans-serif'
      }
  },

  'legend': {
      'itemStyle': {
          'font': '1rem Trebuchet MS, Verdana, sans-serif',
          'color': 'black'
      },
      'itemHoverStyle': {
          'color': 'gray'
      }
  }
}


class Highchart(VisualizationTemplate):
    def __init__(
            self,
            data=None,
            style: str = 'column',
            theme: dict = None,
            setup: dict = None,
            **kwargs
    ):
        super(Highchart, self).__init__(data)
        self.dict = self.__init_highchart_parameters(setup)
        self.__set_style(style)
        self.__set_additional_kwargs(kwargs)
        self.__set_theme(theme)

    @staticmethod
    def __init_highchart_parameters(setup):
        default_dict = {
            'chart': {},
            'legend': {},
            'plotOptions': {},
            'series': [],
            'xAxis': {},
            'yAxis': {}
        }
        setup = {} if setup is None else setup
        return dict(ChainMap(setup, default_dict))

    def __set_theme(self, theme):
        def set_on_position(current_position, current_dict):
            for key, value in current_dict.items():
                if key not in current_position:
                    current_position[key] = value
                else:
                    if isinstance(value, dict):
                        set_on_position(current_position[key], value)

        if theme is None:
            return
        set_on_position(self.dict, theme)

    def render(self, div_id=None, div_kwargs=None):
        div, div_id = self.__create_div(div_id, div_kwargs)
        self.__set_value('renderTo', div_id)
        return HC_Renderer(div, self.__script)

    @property
    def __style(self):
        return self.dict['chart'].get('type')

    @property
    def __script(self):
        hc_json = json.dumps(self.dict)
        script = (
            '<script type="text/javascript">'
            'new Highcharts.Chart({0});'
            '</script>'
        ).format(hc_json)
        return script

    def set_data(self, data):
        self.dict['series'] = []
        if isinstance(data, pandas.Series):
            self.dict['series'].append(
                {'name': data.name, 'data': data.values.tolist()}
            )
        elif isinstance(data, pandas.DataFrame):
            for column in data.columns:
                if self.__style == 'scatter':
                    series_data = [data[column].tolist()]
                elif self.__style == 'line':
                    series_data = data[column][0]
                else:
                    series_data = data[column].tolist()
                series = {
                    'name': column,
                    'data': series_data
                }
                self.dict['series'].append(series)
        else:
            self.dict['series'].append({'data': data})
        if (
                isinstance(data, pandas.Series) or
                isinstance(data, pandas.DataFrame) and
                self.__style != 'scatter'
        ):
            self.dict['xAxis'] = {'categories': data.index.values.tolist()}

    def __set_style(self, style):
        if style == 'bar':
            warn('Highcharts uses keyword "column" instead of "bar" for '
                 'vertical bar charts')
        self.__set_value('style', style)

    def __set_additional_kwargs(self, kwargs):
        for key, value in kwargs.items():
            self.__set_value(key, value)

    def __set_value(self, key, value):
        if key not in hc_kwargs:
            warn(
                'Keyword "' + key + '" not in current accepted keywords. '
                'Key will be neglected.'
            )
            return
        self.__insert_value(value, hc_kwargs[key])

    def __insert_value(self, value, hierarchy: list):
        if len(hierarchy) == 0:
            warn('Can not set value at base level of dict!')
            return

        current_level = []
        for level in hierarchy[:-1]:
            current_level.append(level)
            if reduce(dict.get, current_level, self.dict) is None:
                reduce(dict.get, current_level[:-1], self.dict)[level] = {}
        reduce(dict.get, current_level, self.dict)[hierarchy[-1]] = value

    def __str__(self):
        renderer = self.render()
        return mark_safe(renderer.div + '\n' + renderer.script)

    def __create_div(self, div_id, div_kwargs):
        if div_id is None:
            div_id = 'vis_' + str(self.id)
        params = ''
        if div_kwargs is not None:
            params = ' ' + ' '.join(
                [k + '="' + v + '"' for k, v in div_kwargs.items()])
        div = f'<div id="' + div_id + '"' + params + '></div>'
        return div, div_id
