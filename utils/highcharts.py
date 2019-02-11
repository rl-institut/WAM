
import pandas
import json
from collections import namedtuple, ChainMap
from functools import reduce
from warnings import warn
from highcharts import Highchart as HC
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
  'credits': {
      'enabled': False
  },
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


class Highchart(HC):
    def __init__(self, data=None, options=None, **kwargs):
        super(Highchart, self).__init__()
        if options is not None:
            self.set_dict_options(options)
        if data is not None:
            self.add_pandas_data_set(data, **kwargs)

    def render(self):
        self.buildcontent()
        return self._htmlcontent.decode('utf-8')

    def __str__(self):
        return mark_safe(self.render())

    def add_pandas_data_set(self, data, series_type='column', name=None):
        hc_data = []
        if isinstance(data, pandas.Series):
            hc_data.append(
                {'name': data.name, 'data': data.values.tolist()}
            )
        elif isinstance(data, pandas.DataFrame):
            for column in data.columns:
                if series_type == 'scatter':
                    series_data = [data[column].tolist()]
                elif series_type == 'line':
                    series_data = data[column].tolist()
                else:
                    series_data = data[column].tolist()
                series = {
                    'name': column,
                    'data': series_data
                }
                hc_data.append(series)
        else:
            hc_data.append({'data': data})
        self.add_data_set(hc_data, series_type, name)
