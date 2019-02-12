
import pandas
from highcharts import Highchart as HC
from django.utils.safestring import mark_safe
from django.forms.renderers import get_default_renderer


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
    media_template = 'includes/highchart_media.html'

    def __init__(self, data=None, options=None, **kwargs):
        super(Highchart, self).__init__()
        self.set_dict_options(RLI_THEME)
        if options is not None:
            self.set_dict_options(options)
        if data is not None:
            self.add_pandas_data_set(data, **kwargs)

    def add_pandas_data_set(self, data, series_type='column'):
        if isinstance(data, pandas.Series):
            self.add_data_set(data, series_type, data.name)
        elif isinstance(data, pandas.DataFrame):
            for column in data.columns:
                if series_type == 'scatter':
                    self.add_data_set(
                        [data[column].tolist()],
                        series_type,
                        column
                    )
                else:
                    self.add_data_set(
                        data[column].tolist(),
                        series_type, column
                    )
        else:
            self.add_data_set(data, series_type)
        if (
                isinstance(data, pandas.Series) or
                isinstance(data, pandas.DataFrame) and
                series_type != 'scatter'
        ):
            self.set_options(
                'xAxis',
                {'categories': data.index.values.tolist()}
            )

    def __str__(self):
        self.buildhtml()
        return mark_safe(self.container)

    def media(self):
        context = {'chart': self}
        renderer = get_default_renderer()
        return mark_safe(renderer.render(self.media_template, context))
