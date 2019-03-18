
from itertools import count
import pandas
from highcharts import Highchart as HC
from django.utils.safestring import mark_safe
from django.forms.renderers import get_default_renderer


# Full HC API reference: https://api.highcharts.com/highcharts/
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
            'font': 'bold 1.2rem Roboto, "Trebuchet MS", Verdana, sans-serif'
        }
    },
    'subtitle': {
        'style': {
            'color': '#666',
            'font': 'bold 12px "Roboto Light", "Trebuchet MS", Verdana, sans-serif'
        }
    },
    'lang': {
        'decimalPoint': ',',
        'thousandsSep': '.'
    },
    'legend': {
        'itemStyle': {
            'font': '1rem "Roboto Light", Trebuchet MS, Verdana, sans-serif',
            'color': 'black'
        },
        'itemHoverStyle': {
            'color': 'gray'
        }
    },
    'plotOptions': {
        'series': {
            'dataLabels': {
                'style': {
                    'fontWeight': None,
                    'textOutline': None
                }
            }
        }
    }
}


class Highchart(HC):
    media_template = 'includes/highchart_media.html'
    id_counter = count()

    def __init__(self, use_rli_theme=True, **kwargs):
        self.id = next(self.id_counter)
        if 'renderTo' not in kwargs:
            kwargs['renderTo'] = f'hc_{self.id}'
        super(Highchart, self).__init__(**kwargs)
        if use_rli_theme:
            self.set_dict_options(RLI_THEME)

    def add_pandas_data_set(self, data, series_type=None, **kwargs):
        if series_type is None:
            ValueError('No highcharts type specified.')
        if isinstance(data, pandas.Series):
            self.add_data_set(
                data.values.tolist(), series_type, data.name, **kwargs)
        elif isinstance(data, pandas.DataFrame):
            for column in data.columns:
                if series_type == 'scatter':
                    self.add_data_set(
                        data=[data[column].tolist()],
                        series_type=series_type,
                        name=column,
                        **kwargs
                    )
                else:
                    self.add_data_set(
                        data=data[column].tolist(),
                        series_type=series_type,
                        name=column,
                        **kwargs
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
