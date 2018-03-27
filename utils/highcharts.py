
import pandas
import json
from collections import namedtuple
from functools import reduce
from warnings import warn

HC_Renderer = namedtuple('HighchartsRenderer', ['div', 'script'])


hc_kwargs = {
    'style': ['chart', 'type'],
    'title': ['title', 'text'],
    'renderTo': ['chart', 'renderTo'],
    'x_title': ['xAxis', 'title', 'text'],
    'y_title': ['yAxis', 'title', 'text'],
    'stacked': ['plotOptions', 'series', 'stacking'],
}


class Highchart(object):
    id_counter = 0

    def __init__(
            self,
            data: [pandas.Series, pandas.DataFrame],
            style: str='column',
            **kwargs
    ):
        self.id = self.id_counter
        self.__class__.id_counter += 1
        self.__dict = {
            'chart': {},
            'legend': {},
            'plotOptions': {},
            'series': [],
            'xAxis': {},
            'yAxis': {}
        }
        self.__set_style(style)
        self.__set_data(data)
        self.__set_additional_kwargs(kwargs)

    def render(self, div_id=None):
        div, div_id = self.__div(div_id)
        self.__set_value('renderTo', div_id)
        return HC_Renderer(div, self.__script)

    def __div(self, div_id: str=None):
        if div_id is None:
            div_id = 'hc_' + str(self.id)
        div = '<div id=' + div_id + '></div>'
        return div, div_id

    @property
    def __script(self):
        hc_json = json.dumps(self.__dict)
        script = (
            '<script type="text/javascript">'
            'new Highcharts.Chart({0});'
            '</script>'
        ).format(hc_json)
        return script

    def __set_data(self, data):
        if isinstance(data, pandas.Series):
            self.__dict['series'].append(
                {'name': data.name, 'data': data.values.tolist()}
            )
        elif isinstance(data, pandas.DataFrame):
            for column in data.columns:
                series = {
                    'name': column,
                    'data': data[column].tolist()
                }
                self.__dict['series'].append(series)
        else:
            self.__dict['series'].append({'data': data})
        if (
                isinstance(data, pandas.Series) or
                isinstance(data, pandas.DataFrame)
        ):
            self.__dict['xAxis'] = {'categories': data.index.values.tolist()}

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
            if reduce(dict.get, current_level, self.__dict) is None:
                reduce(dict.get, current_level[:-1], self.__dict)[level] = {}
        reduce(dict.get, current_level, self.__dict)[hierarchy[-1]] = value


if __name__ == '__main__':
    df = pandas.DataFrame(
        {'a': range(3), 'b': range(4, 7)},
        index=['c', 'd', 'e']
    )
    print(df)
    hc = Highchart(df, 'column', stacked=True)
    print(hc.render('hc'))
